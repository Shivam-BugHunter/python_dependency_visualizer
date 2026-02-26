"""
Graph analysis utilities for dependency graphs.
"""

from pathlib import Path
from typing import Dict, List, Optional

from dpv.graph import DependencyGraph


def find_cycles(graph: DependencyGraph) -> List[List[str]]:
    """Detect cycles in dependency graph using DFS."""
    cycles = []
    visited = set()
    rec_stack = set()
    path = []

    def dfs(node: str):
        if node in rec_stack:
            idx = path.index(node)
            cycle = path[idx:] + [node]

            cycle_nodes = cycle[:-1]
            if cycle_nodes:
                min_idx = min(range(len(cycle_nodes)), key=lambda i: cycle_nodes[i])
                normalized = cycle_nodes[min_idx:] + cycle_nodes[:min_idx] + [cycle_nodes[min_idx]]
                cycles.append(normalized)
            return

        if node in visited:
            return

        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for n in graph.neighbors(node):
            dfs(n)

        path.pop()
        rec_stack.remove(node)

    for n in graph.nodes():
        if n not in visited:
            dfs(n)

    # Deduplicate normalized cycles
    seen = set()
    uniq = []
    for cy in cycles:
        tup = tuple(cy[:-1])
        if tup not in seen:
            uniq.append(cy)
            seen.add(tup)

    return uniq


def find_dead_modules(graph: DependencyGraph, entrypoints: Optional[List[str]] = None) -> List[str]:
    """Modules with no incoming edges."""
    if entrypoints is None:
        entrypoints = []

    entry = set(entrypoints)

    indegree = {n: 0 for n in graph.nodes()}

    for n in graph.nodes():
        for neigh in graph.neighbors(n):
            indegree[neigh] = indegree.get(neigh, 0) + 1

    dead = [n for n, deg in indegree.items() if deg == 0 and n not in entry]

    return sorted(dead)


def compute_module_metrics(
    graph: DependencyGraph,
    path_map: Optional[Dict[str, Path]] = None
) -> Dict[str, Dict]:
    """Compute in/out degree & file line counts."""
    metrics = {}

    indegree = {n: 0 for n in graph.nodes()}
    for n in graph.nodes():
        for neigh in graph.neighbors(n):
            indegree[neigh] = indegree.get(neigh, 0) + 1

    for n in graph.nodes():
        m = {
            "in_degree": indegree.get(n, 0),
            "out_degree": len(graph.neighbors(n)),
        }

        if path_map and n in path_map:
            p = path_map[n]
            if isinstance(p, Path) and p.exists():
                try:
                    m["lines"] = sum(1 for _ in p.open("r", encoding="utf-8"))
                except Exception:
                    pass

        metrics[n] = m

    return metrics