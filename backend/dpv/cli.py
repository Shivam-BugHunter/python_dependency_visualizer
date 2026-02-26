"""
Command Line Interface for the DPV (Dependency Project Visualizer)
"""

import argparse
from pathlib import Path
from typing import Optional

from dpv.scanner import iter_py_files
from dpv.parser import parse_imports
from dpv.resolver import build_module_map
from dpv.graph import build_graph
from dpv.analyzer import find_cycles, find_dead_modules, compute_module_metrics
from dpv.output import write_json


def run_scan(folder: str, json_path: Optional[str]):
    """
    Scan a folder for python files, build dependency graph,
    analyze cycles + dead modules, and optionally output JSON.
    """

    root = Path(folder).resolve()
    print(f"📂 Scanning: {root}")

    # 1) collect python files
    py_files = list(iter_py_files(root))
    print(f"📄 Python files found: {len(py_files)}")

    # 2) build module path map
    module_map = build_module_map(root)

    # 3) parse all imports
    import_records_by_file = {}
    for f in py_files:
        import_records_by_file[str(f)] = parse_imports(f, root)

    # 4) build dependency graph
    graph = build_graph(import_records_by_file, module_map)

    # 5) analysis
    cycles = find_cycles(graph)
    dead_modules = find_dead_modules(graph)
    metrics = compute_module_metrics(graph, module_map)

    # 6) summary printing
    print(f"📦 Modules: {len(graph.nodes())}")
    print(f"🔗 Edges: {sum(len(graph.neighbors(n)) for n in graph.nodes())}")
    print(f"🔁 Cycles found: {len(cycles)}")
    print(f"🪦 Dead modules: {len(dead_modules)}")

    # 7) write JSON if requested
    if json_path:
        output_data = {
            "graph": graph.to_adjacency_dict(),
            "cycles": cycles,
            "dead_modules": dead_modules,
            "metrics": metrics,
            "files_scanned": len(py_files),
            "imports_found": sum(len(v) for v in import_records_by_file.values())
        }

        write_json(json_path, output_data)
        print(f"💾 Report saved → {json_path}")


def run_report(json_path: str):
    """Load and pretty-print a report.json."""
    from dpv.output import read_json

    obj = read_json(json_path)
    print(obj)


def main():
    parser = argparse.ArgumentParser(description="DPV - Dependency Project Visualizer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # scan command
    scan = sub.add_parser("scan", help="Scan a folder and generate dependency report")
    scan.add_argument("folder", help="Folder to scan")
    scan.add_argument("--json", help="Output JSON file")

    # report command
    rep = sub.add_parser("report", help="Pretty print a JSON report")
    rep.add_argument("json_path", help="Path to report.json")

    args = parser.parse_args()

    if args.cmd == "scan":
        run_scan(args.folder, args.json)

    elif args.cmd == "report":
        run_report(args.json_path)


if __name__ == "__main__":
    main()