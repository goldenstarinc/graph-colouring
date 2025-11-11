import time, random
from graph_coloring.algorithms.base import ColoringAlgorithm

class GreedyAlgorithm(ColoringAlgorithm):
    """Жадный алгоритм раскраски графа."""
    def __init__(self, order_strategy='degree_desc'):
        super().__init__(name="Greedy")
        self.order_strategy = order_strategy

    def run(self, graph):
        start = time.time()
        vertices = graph.vertices()

        if self.order_strategy == 'degree_desc':
            order = sorted(vertices, key=lambda v: -graph.degree(v))
        elif self.order_strategy == 'random':
            order = vertices[:]
            random.shuffle(order)
        else:  # 'as_loaded'
            order = vertices

        color = {}
        for v in order:
            used = {color[u] for u in graph.neighbors(v) if u in color}
            c = 1
            while c in used:
                c += 1
            color[v] = c

        return {"coloring": color, "colors_used": max(color.values()) if color else 0, "time": time.time() - start}