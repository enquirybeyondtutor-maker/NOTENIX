FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libffi-dev libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV CHROMA_PERSIST_DIR=/data/chroma

EXPOSE 8000

# Render injects $PORT — fall back to 8000 for local/Railway
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
