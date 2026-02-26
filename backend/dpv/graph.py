"""Dependency graph representation and construction."""

from pathlib import Path
from typing import Dict, List, Optional, Set

from dpv.models import ImportRecord
# resolver import is OPTIONAL — Step 5 must not depend on resolver
try:
    from dpv.resolver import resolve_import
except ImportError:
    resolve_import = None


class DependencyGraph:
    """Directed graph representing module dependencies."""

    def __init__(self):
        self.adj: Dict[str, Set[str]] = {}
        self.meta: Dict[str, Dict] = {}

    def add_node(self, name: str, meta: dict = None):
        """Add a node to the graph."""
        if name not in self.adj:
            self.adj[name] = set()
        if meta is not None:
            self.meta[name] = meta.copy()

    def add_edge(self, a: str, b: str):
        """Add directed edge a -> b."""
        self.add_node(a)
        self.add_node(b)
        self.adj[a].add(b)

    def neighbors(self, node: str) -> List[str]:
        return sorted(self.adj.get(node, set()))

    def nodes(self) -> List[str]:
        return sorted(self.adj.keys())

    def to_adjacency_dict(self) -> Dict[str, List[str]]:
        return {n: self.neighbors(n) for n in self.nodes()}


def build_graph(
    import_records_by_file: Dict[str, List[ImportRecord]],
    module_map: Optional[Dict[str, Path]] = None
) -> DependencyGraph:
    """
    Build a dependency graph from parsed import records.

    If module_map is None, we treat record.module as a raw dependency STR.
    This is enough for Step 5 testing and for simple projects.

    If module_map is provided and resolve_import is available,
    we attempt to resolve module names to real dotted module identifiers.
    """
    graph = DependencyGraph()

    for source_key, records in import_records_by_file.items():
        graph.add_node(source_key)

        for record in records:
            raw_mod = record.module

            # Skip invalid blank modules
            if not raw_mod:
                continue

            if module_map and resolve_import:
                from_path = Path(record.file)
                resolved = resolve_import(raw_mod, from_path, module_map)
                if resolved:
                    graph.add_edge(source_key, resolved)
            else:
                # Step 5: no resolver, use raw module names
                graph.add_edge(source_key, raw_mod)

    return graph