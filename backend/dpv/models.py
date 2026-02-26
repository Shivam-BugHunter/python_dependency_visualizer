"""Data models for dependency analysis."""

from dataclasses import dataclass
from typing import List, Literal


@dataclass
class ImportRecord:
    """Represents a single import statement in a Python module.
    
    Attributes:
        typ: Type of import - "import", "from", or "dynamic"
        module: The module being imported from
        names: List of names being imported
        lineno: Line number where the import occurs
        file: Path to the file containing the import
    """
    typ: Literal["import", "from", "dynamic"]
    module: str
    names: List[str]
    lineno: int
    file: str
    
    def __repr__(self) -> str:
        """Return a helpful string representation."""
        names_str = ", ".join(self.names) if self.names else "[]"
        return (
            f"ImportRecord(typ={self.typ!r}, module={self.module!r}, "
            f"names=[{names_str}], lineno={self.lineno}, file={self.file!r})"
        )


@dataclass
class ModuleInfo:
    """Represents information about a Python module.
    
    Attributes:
        name: Module name
        path: File path to the module
        imports: List of import records found in the module
        lines: Total number of lines in the module
    """
    name: str
    path: str
    imports: List[ImportRecord]
    lines: int
    
    def __repr__(self) -> str:
        """Return a helpful string representation."""
        imports_count = len(self.imports)
        return (
            f"ModuleInfo(name={self.name!r}, path={self.path!r}, "
            f"imports=[{imports_count} items], lines={self.lines})"
        )


def record_to_tuple(rec: ImportRecord) -> tuple:
    """Convert an ImportRecord to a tuple for testing purposes.
    
    Args:
        rec: The ImportRecord to convert
        
    Returns:
        A tuple containing (typ, module, tuple(names), lineno, file)
    """
    return (rec.typ, rec.module, tuple(rec.names), rec.lineno, rec.file)

