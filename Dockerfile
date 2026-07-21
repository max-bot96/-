FROM python:3.13-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir .

CMD uvicorn apps.api.main:app --host 0.0.0.0 --port ${PORT:-8000}
