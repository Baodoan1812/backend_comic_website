# --- Dockerfile ---
    FROM python:3.11-slim

    # Đặt thư mục làm việc trong container
    WORKDIR /app
    
    # Tắt cache và buffer của Python
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    # Copy và cài dependencies
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy toàn bộ project vào container
    COPY . .
    
    # Đặt thư mục làm việc bên trong container là nơi có manage.py
    WORKDIR /app/core
    
    # Expose cổng mặc định của Django
    EXPOSE 8000
    
    # Lệnh chạy server
    CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
    