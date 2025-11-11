import csv
from graph_coloring.graph_model import GraphModel

def load_edgelist(path):
    edges = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                u, v = parts[:2]
                try:
                    u, v = int(u), int(v)
                except:
                    pass
                edges.append((u, v))
    return GraphModel.from_edgelist(edges)

def export_coloring(path, coloring):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['vertex', 'color'])
        for v, c in coloring.items():
            w.writerow([v, c])

def save_report_txt(path, *, algorithm_name, order_strategy, n, m, colors_used, time_sec, coloring):
    """
    Сохраняет текстовый отчёт с параметрами и метриками (в формате, близком к описанному в главе).
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write("Отчёт по раскраске графа\n")
        f.write("=======================\n\n")
        f.write(f"Алгоритм: {algorithm_name}\n")
        f.write(f"Порядок обхода (order_strategy): {order_strategy}\n")
        f.write(f"Число вершин: {n}\n")
        f.write(f"Число рёбер: {m}\n")
        f.write(f"Использовано цветов: {colors_used}\n")
        f.write(f"Время выполнения (сек): {time_sec:.6f}\n\n")
        f.write("Раскраска (вершина -> цвет):\n")
        for v, c in sorted(coloring.items(), key=lambda x: str(x[0])):
            f.write(f"{v}\t{c}\n")