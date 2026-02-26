# DPV - Python Dependency Analyzer

A lightweight command-line tool for analyzing Python project dependencies, detecting circular imports, and identifying dead code.

## Overview

DPV (Dependency Python Viewer) is a static analysis tool that scans Python projects to build dependency graphs, detect circular dependencies, and identify unused modules. It uses AST parsing to extract import statements and provides multiple output formats for visualization and analysis.

## Features

- **📁 File Scanning**: Recursively scans Python projects, automatically skipping virtual environments and hidden directories
- **🔍 Import Extraction**: Parses Python files using AST to extract:
  - Standard imports (`import x`)
  - From imports (`from x import y`)
  - Relative imports (`from . import z`)
  - Dynamic imports (`__import__()`, `importlib.import_module()`)
- **📊 Dependency Graph**: Builds directed dependency graphs from import relationships
- **🔄 Cycle Detection**: Identifies circular dependencies in your codebase
- **💀 Dead Code Detection**: Finds modules with no incoming dependencies (unused code)
- **🌳 ASCII Tree Visualization**: Displays dependency trees in a readable ASCII format
- **📈 Multiple Export Formats**: Supports DOT format for Graphviz and JSON reports
- **🎯 Module Resolution**: Resolves relative imports to absolute module names

## Installation

### From Source

```bash
git clone <repository-url>
cd dpv-project
pip install -e .
```

### Requirements

- Python 3.10 or higher
- No external dependencies (uses only Python standard library)

## CLI Usage Examples

### Scan Project

Scan a directory and get a summary of files and imports:

```bash
dpv scan /path/to/project
```

**Output:**
```
Scanned 15 files, found 42 imports.
```

### Visualize Dependency Graph

Print an ASCII tree of dependencies:

```bash
dpv graph /path/to/project --ascii
```

**Example Output:**
```
└── main.py
    ├── utils.py
    │   └── os
    └── config.py
        └── json
```

### Export to DOT Format

Generate a Graphviz DOT file for visualization:

```bash
dpv graph /path/to/project --dot dependencies.dot
dot -Tpng dependencies.dot -o dependencies.png
```

### Generate Analysis Report

Create a JSON report with cycles and dead modules:

```bash
dpv report /path/to/project --json report.json
```

**Output:**
```
Report written to report.json
```

Or print a summary to console:

```bash
dpv report /path/to/project
```

**Example Output:**
```
Cycles found: 2
Dead modules: 3

Cycles:
  module_a -> module_b -> module_a
  module_x -> module_y -> module_z -> module_x

Dead modules: unused.py, legacy.py, test_old.py
```

## Screenshots

### ASCII Dependency Tree
```
<!-- Screenshot: ASCII tree visualization -->
```

### Graphviz Visualization
```
<!-- Screenshot: Graphviz-generated dependency graph -->
```

### JSON Report
```
<!-- Screenshot: JSON report structure -->
```

## Architecture

DPV is organized into modular components:

```
dpv/
├── scanner.py      # File discovery and reading
├── parser.py       # AST-based import extraction
├── models.py       # Data models (ImportRecord, ModuleInfo)
├── resolver.py     # Module name resolution
├── graph.py        # Dependency graph construction
├── analyzer.py     # Graph analysis (cycles, dead code, metrics)
├── output.py       # Output formatting (ASCII, DOT, JSON)
└── cli.py          # Command-line interface
```

### Data Flow

1. **Scanning**: `scanner.iter_py_files()` discovers Python files
2. **Parsing**: `parser.extract_imports()` extracts import statements using AST
3. **Resolution**: `resolver.build_module_map()` and `resolver.resolve_import()` resolve module names
4. **Graph Building**: `graph.build_graph()` constructs the dependency graph
5. **Analysis**: `analyzer.find_cycles()` and `analyzer.find_dead_modules()` perform analysis
6. **Output**: `output` module formats results (ASCII, DOT, JSON)

### Key Design Decisions

- **Pure Python Standard Library**: No external dependencies for maximum compatibility
- **AST-Based Parsing**: Accurate import detection without executing code
- **Lazy Resolution**: Module resolution is optional, allowing analysis without full project structure
- **Extensible Graph Model**: Simple adjacency list structure for easy analysis

## Limitations

- **Static Analysis Only**: Cannot detect dynamically constructed import paths (e.g., `__import__(variable_name)`)
- **No Type Checking**: Does not analyze type hints or type dependencies
- **Limited Dynamic Import Detection**: Only detects `__import__()` and `importlib.import_module()` with string literals
- **No Cross-Language Support**: Python-only (no analysis of C extensions or other languages)
- **Relative Import Resolution**: Requires proper package structure with `__init__.py` files
- **No Dependency Versioning**: Does not track package versions or requirements.txt

## Future Improvements

- [ ] Support for `requirements.txt` and `pyproject.toml` dependency analysis
- [ ] Integration with package managers (pip, poetry, conda)
- [ ] Web-based visualization interface
- [ ] Incremental analysis for large codebases
- [ ] Export to additional formats (SVG, PDF, Mermaid)
- [ ] Support for namespace packages (PEP 420)
- [ ] Detection of unused imports within files
- [ ] Integration with CI/CD pipelines
- [ ] Performance metrics and optimization suggestions
- [ ] Support for async import patterns

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

