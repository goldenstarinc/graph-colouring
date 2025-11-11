import unittest
from graph_coloring.graph_model import GraphModel
from graph_coloring.algorithms.greedy import GreedyAlgorithm
from graph_coloring.algorithms.dsatur import DSATURAlgorithm
from graph_coloring.io_module import export_coloring, load_edgelist, save_report_txt
import tempfile, os

class TestGraphColoring(unittest.TestCase):
    def setUp(self):
        self.edges = [(1, 2), (2, 3), (1, 3)]
        self.graph = GraphModel.from_edgelist(self.edges)

    def test_graph_vertices_and_edges(self):
        self.assertEqual(self.graph.n(), 3)
        self.assertEqual(self.graph.m(), 3)

    def test_neighbors(self):
        self.assertEqual(self.graph.neighbors(1), {2, 3})

    def test_greedy_coloring(self):
        algo = GreedyAlgorithm(order_strategy='degree_desc')
        res = algo.run(self.graph)
        self.assertIn("coloring", res)
        self.assertGreaterEqual(res["colors_used"], 1)

    def test_dsatur_coloring(self):
        algo = DSATURAlgorithm()
        res = algo.run(self.graph)
        self.assertIn("coloring", res)
        self.assertGreaterEqual(res["colors_used"], 1)

    def test_no_edges_graph(self):
        g = GraphModel()
        for i in range(5):
            g.add_vertex(i)
        res = DSATURAlgorithm().run(g)
        self.assertEqual(res["colors_used"], 1)

    def test_load_and_export_coloring(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp:
            for u, v in self.edges:
                tmp.write(f"{u} {v}\n")
            tmp_path = tmp.name

        g2 = load_edgelist(tmp_path)
        os.remove(tmp_path)
        self.assertEqual(g2.m(), 3)

        res = GreedyAlgorithm().run(g2)
        tmp_csv = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        tmp_csv.close()
        export_coloring(tmp_csv.name, res["coloring"])
        self.assertTrue(os.path.exists(tmp_csv.name))
        os.remove(tmp_csv.name)

    def test_save_report_txt(self):
        res = DSATURAlgorithm().run(self.graph)
        tmp_report = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        tmp_report.close()
        save_report_txt(tmp_report.name,
                        algorithm_name="DSATUR",
                        order_strategy="degree_desc",
                        n=self.graph.n(),
                        m=self.graph.m(),
                        colors_used=res["colors_used"],
                        time_sec=res["time"],
                        coloring=res["coloring"])
        self.assertTrue(os.path.getsize(tmp_report.name) > 0)
        os.remove(tmp_report.name)

    def test_subgraph(self):
        sub = self.graph.subgraph([1, 2])
        self.assertEqual(sub.m(), 1)
        self.assertIn(2, sub.neighbors(1))

    def test_greedy_random_order(self):
        algo = GreedyAlgorithm(order_strategy='random')
        res = algo.run(self.graph)
        self.assertTrue(isinstance(res["coloring"], dict))

    def test_empty_graph(self):
        g = GraphModel()
        res = DSATURAlgorithm().run(g)
        self.assertEqual(res["colors_used"], 0)
        self.assertEqual(res["coloring"], {})

if __name__ == "__main__":
    unittest.main()
