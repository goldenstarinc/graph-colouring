# gui_app.py
import tkinter as tk
from tkinter import filedialog, messagebox
import math, time
import os

from graph_coloring.io_module import load_edgelist, export_coloring, save_report_txt
from graph_coloring.algorithms.dsatur import DSATURAlgorithm
from graph_coloring.algorithms.greedy import GreedyAlgorithm

class GUIApp:
    """GUI для визуализации раскраски графа (DSATUR и Greedy)."""
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Coloring (DSATUR + Greedy)")
        self.graph = None
        self.coloring = {}
        self.last_result = None

        # Панель управления
        frame = tk.Frame(root)
        frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Загрузка графа
        tk.Button(frame, text="Загрузить граф (.txt)", command=self.load_graph).pack(fill=tk.X, pady=2)

        # Выбор алгоритма
        self.algo = tk.StringVar(value="DSATUR")
        tk.Label(frame, text="Выбор алгоритма:").pack(anchor="w", pady=(5, 0))
        tk.Radiobutton(frame, text="DSATUR", variable=self.algo, value="DSATUR").pack(anchor="w")
        tk.Radiobutton(frame, text="Greedy", variable=self.algo, value="Greedy").pack(anchor="w")

        # Стратегия обхода вершин
        tk.Label(frame, text="Порядок обхода вершин:").pack(anchor="w", pady=(8, 0))
        self.order_strategy = tk.StringVar(value="degree_desc")
        strategies = ["degree_desc", "random", "as_loaded"]
        for s in strategies:
            tk.Radiobutton(frame, text=s, variable=self.order_strategy, value=s).pack(anchor="w")

        # Кнопка запуска
        tk.Button(frame, text="Запустить алгоритм", command=self.run_algo).pack(fill=tk.X, pady=5)

        # Экспорт кнопки
        tk.Button(frame, text="Сохранить раскраску (CSV)", command=self.save_coloring_dialog).pack(fill=tk.X, pady=2)
        tk.Button(frame, text="Сохранить отчёт (.txt)", command=self.save_report_dialog).pack(fill=tk.X, pady=2)

        # Статистика
        self.stats_label = tk.Label(frame, text="n=0, m=0\ncolors=0\ntime=0.000s")
        self.stats_label.pack(pady=10)

        # Канвас для отрисовки
        self.canvas = tk.Canvas(root, width=700, height=600, bg="white")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    # Загрузка графа
    def load_graph(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.graph = load_edgelist(path)
            if not self.graph or len(self.graph.adj) == 0:
                raise Exception("Файл пуст.");
            self._draw_graph(colorful=False)
            messagebox.showinfo("Загружено", f"Граф успешно загружен из файла:\n{os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить граф:\n{e}")

    # Запуск алгоритма
    def run_algo(self):
        if not self.graph:
            messagebox.showwarning("Нет графа", "Сначала загрузите граф из файла.")
            return

        algo_name = self.algo.get()
        order_strategy = self.order_strategy.get()

        start = time.time()
        if algo_name == "DSATUR":
            res = DSATURAlgorithm().run(self.graph)
        else:
            res = GreedyAlgorithm(order_strategy=order_strategy).run(self.graph)

        elapsed = time.time() - start

        self.coloring = res["coloring"]
        self.last_result = {
            "algorithm": algo_name,
            "order_strategy": order_strategy,
            "n": self.graph.n(),
            "m": self.graph.m(),
            "colors_used": res["colors_used"],
            "time": res["time"],
            "coloring": self.coloring
        }

        self._draw_graph(colorful=True)
        self.stats_label.config(
            text=f"n={self.graph.n()}, m={self.graph.m()}\n"
                 f"colors={res['colors_used']}\ntime={res['time']:.4f}s"
        )

    # Сохранение раскраски
    def save_coloring_dialog(self):
        if not self.coloring:
            messagebox.showinfo("Нет данных", "Сначала выполните алгоритм.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")],
                                            title="Сохранить раскраску")
        if not path:
            return
        try:
            export_coloring(path, self.coloring)
            messagebox.showinfo("Сохранено", f"Результаты раскраски сохранены в:\n{path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить CSV:\n{e}")

    # Сохранение отчёта
    def save_report_dialog(self):
        if not self.last_result:
            messagebox.showinfo("Нет данных", "Сначала выполните алгоритм.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")],
                                            title="Сохранить отчёт (.txt)")
        if not path:
            return
        try:
            save_report_txt(path,
                            algorithm_name=self.last_result["algorithm"],
                            order_strategy=self.last_result["order_strategy"],
                            n=self.last_result["n"],
                            m=self.last_result["m"],
                            colors_used=self.last_result["colors_used"],
                            time_sec=self.last_result["time"],
                            coloring=self.last_result["coloring"])
            messagebox.showinfo("Сохранено", f"Отчёт успешно сохранён в:\n{path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить отчёт:\n{e}")

    # Визуализация графа
    def _draw_graph(self, colorful: bool):
        self.canvas.delete("all")
        if not self.graph:
            return
        vertices = self.graph.vertices()
        n = len(vertices)
        if n == 0:
            return

        positions = {}
        cx, cy, r = 350, 300, min(250, 250 + 200 / max(n, 5))
        for i, v in enumerate(vertices):
            angle = 2 * math.pi * i / n
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            positions[v] = (x, y)

        for v in vertices:
            for u in self.graph.neighbors(v):
                if str(u) < str(v):
                    x1, y1 = positions[v]
                    x2, y2 = positions[u]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#888", width=2)

        for v in vertices:
            x, y = positions[v]
            color = self._color_to_hex(self.coloring.get(v, 0)) if colorful else "#FFFFFF"
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color, outline="black", width=1.5)
            self.canvas.create_text(x, y, text=str(v), font=("Arial", 10, "bold"))

    def _color_to_hex(self, c: int) -> str:
        if c <= 0:
            return "#FFFFFF"
        palette = [
            "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
            "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
            "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
            "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080"
        ]
        return palette[(c - 1) % len(palette)]

# Точка входа
if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
