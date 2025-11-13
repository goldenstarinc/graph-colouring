import sys
import os
from graph_coloring.io_module import load_edgelist, export_coloring
from graph_coloring.algorithms.dsatur import DSATURAlgorithm
from graph_coloring.algorithms.greedy import GreedyAlgorithm

def running_in_docker():
    return os.path.exists('/.dockerenv')

def cli_mode():
    if len(sys.argv) < 3:
        print("Usage: python main.py <graph.txt> <dsatur|greedy>")
        return
    path, algo = sys.argv[1], sys.argv[2]
    g = load_edgelist(path)
    res = DSATURAlgorithm().run(g) if algo == "dsatur" else GreedyAlgorithm().run(g)
    print(f"n={g.n()}, m={g.m()}, colors={res['colors_used']}, time={res['time']:.6f}s")
    export_coloring("coloring.csv", res["coloring"])
    print("Saved to coloring.csv")

def gui_mode():
    import tkinter as tk
    from graph_coloring.gui import GUIApp
    root = tk.Tk()
    GUIApp(root)
    root.mainloop()

if __name__ == "__main__":
    if running_in_docker() or len(sys.argv) > 1:
        cli_mode()
    else:
        gui_mode()