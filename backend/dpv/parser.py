"""
Parse Python import statements using AST and produce ImportRecord objects.

The parser returns a list of dpv.models.ImportRecord instances for each file.
This matches the shape expected by build_graph(...).
"""

from __future__ import annotations
import ast
from pathlib import Path
from typing import List, Optional

from dpv.models import ImportRecord


def _make_import_record(typ: str, module: str, names: List[str], lineno: int, file_path: str) -> ImportRecord:
    # Ensure types align with models.ImportRecord
    return ImportRecord(typ=typ, module=module or "", names=names or [], lineno=lineno or 0, file=file_path)


def _extract_constant_string(node: ast.AST) -> Optional[str]:
    """Return a plain string if node is a constant string (py3.8+: ast.Constant)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    # For older AST variants or explicit Str node
    if isinstance(node, ast.Str):
        return node.s
    return None


def parse_imports(path: Path, root: Path) -> List[ImportRecord]:
    """
    Parse a Python file and return a list of ImportRecord objects.

    Args:
        path: Path to the .py file being parsed
        root: Root directory of the project (unused for now, reserved for resolver logic)

    Returns:
        List[ImportRecord]
    """
    try:
        source = path.read_text(encoding="utf-8")
    except Exception:
        return []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        # Skip files with syntax errors
        return []

    records: List[ImportRecord] = []
    file_str = str(path)

    # Walk AST and capture import statements and some dynamic import patterns
    for node in ast.walk(tree):

        # Handle: import a, b as c
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name  # full dotted name; we'll keep full but build_graph may use first part
                names = [alias.asname] if alias.asname else []
                # For clarity we store the full module as module and the alias name in names (if any)
                rec = _make_import_record(
                    typ="import",
                    module=module_name,
                    names=[alias.name],
                    lineno=getattr(node, "lineno", 0),
                    file_path=file_str
                )
                records.append(rec)

        # Handle: from X import a, b as c
        elif isinstance(node, ast.ImportFrom):
            # compute module string including relative leading dots
            module_part = node.module or ""
            # node.level denotes relative import depth (0 = absolute)
            if getattr(node, "level", 0):
                # Represent relative import as leading dots + module (may be empty)
                rel = "." * node.level
                module_name = rel + module_part
            else:
                module_name = module_part

            # Names imported
            imported_names = [alias.name for alias in node.names]
            rec = _make_import_record(
                typ="from",
                module=module_name,
                names=imported_names,
                lineno=getattr(node, "lineno", 0),
                file_path=file_str
            )
            records.append(rec)

        # Handle simple dynamic import patterns:
        # __import__('module')  or importlib.import_module('module')
        elif isinstance(node, ast.Call):
            # __import__('x')
            func = node.func
            func_name = None
            if isinstance(func, ast.Name):
                func_name = func.id
            elif isinstance(func, ast.Attribute):
                # e.g., importlib.import_module
                if isinstance(func.value, ast.Name):
                    func_name = f"{func.value.id}.{func.attr}"
                else:
                    func_name = func.attr

            if func_name == "__import__":
                # first arg may be a constant string
                if node.args:
                    s = _extract_constant_string(node.args[0])
                    if s:
                        rec = _make_import_record(
                            typ="dynamic",
                            module=s,
                            names=[],
                            lineno=getattr(node, "lineno", 0),
                            file_path=file_str
                        )
                        records.append(rec)

            elif func_name in ("importlib.import_module", "import_module"):
                # importlib.import_module('x')
                if node.args:
                    s = _extract_constant_string(node.args[0])
                    if s:
                        rec = _make_import_record(
                            typ="dynamic",
                            module=s,
                            names=[],
                            lineno=getattr(node, "lineno", 0),
                            file_path=file_str
                        )
                        records.append(rec)

    return records