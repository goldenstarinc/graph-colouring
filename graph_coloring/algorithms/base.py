from abc import ABC, abstractmethod

class ColoringAlgorithm(ABC):
    """Абстрактный базовый класс для алгоритмов раскраски."""
    def __init__(self, name: str = "ColoringAlgorithm"):
        self.name = name

    @abstractmethod
    def run(self, graph):
        """
        Должен возвращать словарь с ключами:
        - "coloring": dict(vertex -> color)
        - "colors_used": int
        - "time": float
        """
        pass