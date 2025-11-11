import time, random
from graph_coloring.algorithms.base import ColoringAlgorithm
from graph_coloring.algorithms.greedy import GreedyAlgorithm

class DSATURAlgorithm(ColoringAlgorithm):
    """Алгоритм DSATUR (Degree of Saturation)."""
    def __init__(self, tie_break='degree_desc'):
        super().__init__(name="DSATUR")
        self.tie_break = tie_break

    def run(self, graph):
        start = time.time()
        uncolored = set(graph.vertices())
        color = {}
        sat = {v: 0 for v in uncolored}
        neigh_colors = {v: set() for v in uncolored}
        degree = {v: graph.degree(v) for v in uncolored}

        if not uncolored:
            return {"coloring": {}, "colors_used": 0, "time": 0.0}

        v0 = max(uncolored, key=lambda v: degree[v])
        color[v0] = 1
        uncolored.remove(v0)
        for u in graph.neighbors(v0):
            neigh_colors[u].add(1)
            sat[u] = len(neigh_colors[u])

        while uncolored:
            v = self._select_vertex(uncolored, sat, degree)
            used = neigh_colors[v]
            c = 1
            while c in used:
                c += 1
            color[v] = c
            uncolored.remove(v)
            for u in graph.neighbors(v):
                if u in uncolored:
                    neigh_colors[u].add(c)
                    sat[u] = len(neigh_colors[u])

        return {"coloring": color, "colors_used": max(color.values()) if color else 0, "time": time.time() - start}

    def _select_vertex(self, uncolored, sat, degree):
        max_sat = max(sat[v] for v in uncolored)
        candidates = [v for v in uncolored if sat[v] == max_sat]
        if len(candidates) == 1:
            return candidates[0]
        if self.tie_break == 'degree_desc':
            return max(candidates, key=lambda v: degree[v])
        return random.choice(candidates)