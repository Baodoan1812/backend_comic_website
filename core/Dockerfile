# --- Dockerfile ---
    FROM python:3.11-slim

    # Đặt thư mục làm việc
    WORKDIR /app
    
    # Tắt cache và buffer của Python
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    # Cài các gói hệ thống cần thiết để psycopg2 hoạt động
    RUN apt-get update && apt-get install -y \
        gcc \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    # Copy và cài dependencies
    COPY requirements.txt .
    RUN pip install --upgrade pip
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy toàn bộ project vào container
    COPY . .
    
    # Expose cổng Django
    EXPOSE 8000
    
    # Chạy migrate rồi runserver
    CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
    