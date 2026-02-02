FROM python:3.11-slim

WORKDIR /app

# sudachipy が Rust を要求するので入れる（ついでにビルド系も）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    rustc \
    cargo \
 && rm -rf /var/lib/apt/lists/*

# pipを新しくして wheel を拾える確率も上げる
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]