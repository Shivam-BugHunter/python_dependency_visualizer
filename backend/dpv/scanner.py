"""File scanning utilities for finding and reading Python files."""

from pathlib import Path
from typing import Iterator


def iter_py_files(root: str | Path) -> Iterator[Path]:
    """Recursively yield .py files under root directory.
    
    Skips paths containing segments: 'venv', '.venv', '.git', '__pycache__'
    and hidden top-level directories starting with '.'.
    
    Args:
        root: Root directory path (str or Path)
        
    Yields:
        Path objects for each .py file found
    """
    root_path = Path(root)
    skip_segments = {'venv', '.venv', '.git', '__pycache__'}
    
    for py_file in root_path.rglob("*.py"):
        # Check if any path segment should be skipped
        parts = py_file.parts
        if any(part in skip_segments for part in parts):
            continue
        
        # Check if top-level directory is hidden (starts with '.')
        if len(parts) > 0:
            # Get the relative path from root to check top-level dir
            try:
                rel_path = py_file.relative_to(root_path)
                if rel_path.parts and rel_path.parts[0].startswith('.'):
                    continue
            except ValueError:
                # If path is not relative to root, skip
                continue
        
        yield py_file


def read_file(path: Path) -> str:
    """Safely read text from a file path.
    
    Returns empty string on error and logs exception via print.
    
    Args:
        path: File path to read
        
    Returns:
        File contents as string, or empty string on error
    """
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

