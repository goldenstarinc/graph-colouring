from typing import Dict, Set, List, Tuple

class GraphModel:
    """Класс неориентированного графа на основе списка смежности."""
    def __init__(self):
        self.adj: Dict[object, Set[object]] = {}

    @classmethod
    def from_edgelist(cls, edges: List[Tuple[object, object]]) -> "GraphModel":
        g = cls()
        for u, v in edges:
            g.add_edge(u, v)
        return g

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = set()

    def add_edge(self, u, v):
        if u == v:
            return
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].add(v)
        self.adj[v].add(u)

    def vertices(self):
        return list(self.adj.keys())

    def neighbors(self, v):
        return self.adj.get(v, set())

    def degree(self, v):
        return len(self.adj.get(v, []))

    def n(self):
        return len(self.adj)

    def m(self):
        return sum(len(n) for n in self.adj.values()) // 2

    def subgraph(self, verts):
        sub = GraphModel()
        for v in verts:
            sub.add_vertex(v)
        for v in verts:
            for u in self.neighbors(v):
                if u in verts:
                    sub.add_edge(v, u)
        return sub