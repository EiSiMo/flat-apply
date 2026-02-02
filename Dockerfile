FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]