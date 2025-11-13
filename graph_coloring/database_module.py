import sqlite3, json, os

class Database:
    def __init__(self, path="graph_data.db"):
        self.path = path
        self._ensure_db()

    def _ensure_db(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS graphs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        n INTEGER,
                        m INTEGER,
                        data TEXT
                     )""")
        c.execute("""CREATE TABLE IF NOT EXISTS colorings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        graph_id INTEGER,
                        algorithm TEXT,
                        order_strategy TEXT,
                        colors_used INTEGER,
                        time_sec REAL,
                        coloring TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )""")
        conn.commit()
        conn.close()

    def add_graph(self, name, n, m, edges):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        edges_str = ",".join([f"{u}-{v}" for u, v in edges])
        c.execute("INSERT INTO graphs (name, n, m, data) VALUES (?, ?, ?, ?)", (name, n, m, edges_str))
        conn.commit()
        conn.close()

    def add_coloring(self, graph_id, algorithm, order_strategy, colors_used, time_sec, coloring):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("""INSERT INTO colorings 
                     (graph_id, algorithm, order_strategy, colors_used, time_sec, coloring)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (graph_id, algorithm, order_strategy, colors_used, time_sec, json.dumps(coloring)))
        conn.commit()
        conn.close()

    def get_graphs(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT id, name, n, m FROM graphs")
        data = c.fetchall()
        conn.close()
        return data

    def get_colorings(self, graph_id):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT algorithm, order_strategy, colors_used, time_sec, coloring, created_at FROM colorings WHERE graph_id=?", (graph_id,))
        data = c.fetchall()
        conn.close()
        return data