# Graph Coloring App (DSATUR + Greedy)

Приложение для визуализации и сравнения алгоритмов раскраски графов на Python.  
Поддерживаются два алгоритма:
- **DSATUR (Degree of Saturation)**
- **Greedy (Жадный алгоритм)**

Проект имеет графический интерфейс (GUI) на `tkinter` и позволяет:
- загружать графы из `.txt` файлов;
- выполнять раскраску выбранным алгоритмом;
- сохранять результаты в `.csv`;
- формировать текстовые отчёты `.txt`.

## Зависимости
Tkinter==0.1.0


## Состав
- **graph_coloring_app.py** — основной код программы с GUI (Tkinter) и CLI.
- **Dockerfile** — контейнер для headless-запуска.

## Локальный запуск
```bash
python3 graph_coloring_app.py
```
или в headless:
```bash
python3 graph_coloring_app.py test
```

## Docker
```bash
docker build -t graph-coloring-app .
docker run --rm graph-coloring-app test
```

При желании можно смонтировать каталог данных и запустить:
```bash
docker run --rm -v /path/to/data:/data graph-coloring-app run /data/edges.txt dsatur
```

## Запуск тестов
```bash
python -m unittest tests.py
```