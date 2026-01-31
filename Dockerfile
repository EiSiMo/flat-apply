FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install the specific browser version required by the playwright version in requirements.txt
RUN playwright install chromium

COPY . .

CMD ["python", "main.py"]
