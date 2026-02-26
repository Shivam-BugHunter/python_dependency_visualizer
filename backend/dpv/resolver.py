"""Module resolution utilities for resolving import statements."""

from pathlib import Path
from typing import Dict, Optional

from dpv.scanner import iter_py_files


def build_module_map(root: Path) -> Dict[str, Path]:
    """Build a mapping of module names to file paths.
    
    Scans recursively for .py files and computes dotted module names
    based on folder structure and presence of __init__.py files.
    
    Args:
        root: Root directory to scan
        
    Returns:
        Dictionary mapping module_name -> file_path
    """
    root_path = Path(root).resolve()
    module_map = {}
    
    for py_file in iter_py_files(root_path):
        try:
            rel_path = py_file.relative_to(root_path)
        except ValueError:
            continue
        
        # Convert path to module name
        parts = list(rel_path.parts)
        
        # Remove .py extension from filename
        if parts[-1].endswith('.py'):
            parts[-1] = parts[-1][:-3]
        
        # If __init__.py, module name is the directory
        if parts[-1] == '__init__':
            parts.pop()
        
        # Build dotted module name
        if parts:
            module_name = '.'.join(parts)
            module_map[module_name] = py_file
    
    return module_map


def resolve_import(module_name: str, from_path: Path, module_map: Dict[str, Path]) -> Optional[str]:
    """Resolve an import statement to an absolute module name.
    
    Handles both absolute and relative imports:
    - Absolute imports: lookup module_name directly in module_map
    - Relative imports: resolve based on leading dots and from_path's package
    
    Args:
        module_name: The import name (may have leading dots for relative imports)
        from_path: Path to the file containing the import
        module_map: Mapping of module names to file paths
        
    Returns:
        Resolved dotted module name or None if not found
    """
    # Handle absolute imports
    if not module_name.startswith('.'):
        return module_name if module_name in module_map else None
    
    # Handle relative imports
    # Count leading dots
    dots = 0
    for char in module_name:
        if char == '.':
            dots += 1
        else:
            break
    
    # Find which module from_path belongs to
    from_path = Path(from_path).resolve()
    current_module = None
    for mod_name, mod_path in module_map.items():
        if Path(mod_path).resolve() == from_path:
            current_module = mod_name
            break
    
    if current_module is None:
        return None
    
    # Get the base module name (without leading dots)
    base_name = module_name[dots:].lstrip('.')
    
    # Split current module into parts and go up 'dots' levels
    parts = current_module.split('.')
    if dots > len(parts):
        return None
    
    # Go up the package hierarchy: remove last 'dots' parts
    parent_parts = parts[:-dots] if dots > 0 else parts
    
    # Build the resolved module name
    if base_name:
        resolved = '.'.join(parent_parts + [base_name]) if parent_parts else base_name
    else:
        resolved = '.'.join(parent_parts) if parent_parts else None
    
    return resolved if resolved and resolved in module_map else None

