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
Tkinter==8.6
Sqlite3==3.44.0

## Состав
- **graph_coloring_app.py** — основной код программы с GUI (Tkinter) и CLI.
- **Dockerfile** — контейнер для headless-запуска.

## Локальный запуск
```bash
python3 main.py
```
или в headless:
```bash
python3 main.py test
```

## Docker
```bash
docker build -t graph-coloring-app .
sudo docker run --rm -v $(pwd)/tests:/data -v $(pwd):/app app /data/1.txt dsatur
```


## Запуск тестов
```bash
python -m unittest tests.py
```