"""
Output utilities for dependency graphs.
Handles ASCII trees, DOT exports, and JSON writing/reading.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, List, Optional

from dpv.graph import DependencyGraph


# ------------------------------------------------------------
# ASCII TREE PRINTER
# ------------------------------------------------------------

def print_ascii_tree(graph: DependencyGraph, roots: Optional[List[str]] = None, depth_limit: int = 5):
    """Print a readable ASCII dependency tree."""
    
    # Auto-detect roots (nodes with indegree 0)
    if roots is None:
        indegree = {node: 0 for node in graph.nodes()}
        for node in graph.nodes():
            for neighbor in graph.neighbors(node):
                indegree[neighbor] = indegree.get(neighbor, 0) + 1
        roots = [node for node, degree in indegree.items() if degree == 0]
        roots = sorted(roots) if roots else graph.nodes()[:1]

    visited_in_path = set()
    visited_printed = set()

    def print_node(node: str, prefix: str = "", is_last: bool = True, depth: int = 0):
        if depth > depth_limit:
            print(f"{prefix}... (depth limit reached)")
            return

        is_cycle = node in visited_in_path
        cycle_marker = " (cycle)" if is_cycle else ""
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{node}{cycle_marker}")

        if is_cycle or node in visited_printed:
            return

        visited_printed.add(node)
        visited_in_path.add(node)

        neighbors = graph.neighbors(node)
        new_prefix = prefix + ("    " if is_last else "│   ")

        for i, neighbor in enumerate(neighbors):
            print_node(neighbor, new_prefix, i == len(neighbors) - 1, depth + 1)

        visited_in_path.remove(node)

    for i, root in enumerate(roots):
        if i > 0:
            print()
        print_node(root)


# ------------------------------------------------------------
# DOT EXPORT
# ------------------------------------------------------------

def export_dot(graph: DependencyGraph, file_path: str):
    """Export graph to DOT format for GraphViz."""
    lines = ["digraph {"]

    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            node_escaped = '"' + node.replace('"', '\\"') + '"'
            neighbor_escaped = '"' + neighbor.replace('"', '\\"') + '"'
            lines.append(f"  {node_escaped} -> {neighbor_escaped};")

    lines.append("}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ------------------------------------------------------------
# GENERIC JSON WRITERS (what CLI expects)
# ------------------------------------------------------------

def write_json(path: str | Path, data: Any) -> None:
    """Write Python data to JSON with pretty indentation."""
    try:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"✔ JSON written to {path}")

    except Exception as e:
        print(f"❌ Error writing JSON to '{path}': {e}")


def read_json(path: str | Path) -> Any:
    """Read JSON from a file safely."""
    try:
        with Path(path).open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON '{path}': {e}")
        return {}


# ------------------------------------------------------------
# DPV REPORT (used by CLI)
# ------------------------------------------------------------

def write_json_report(graph: DependencyGraph, cycles: List[List[str]], dead: List[str], file_path: str):
    """Write full JSON analysis report used by DPV frontend."""
    
    report = {
        "graph": graph.to_adjacency_dict(),
        "cycles": cycles,
        "dead_modules": dead
    }

    write_json(file_path, report)