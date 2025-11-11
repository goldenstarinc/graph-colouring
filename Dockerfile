FROM python:3.10-slim

WORKDIR /app

COPY graph_coloring_app.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "graph_coloring_app.py"]
CMD ["test"]