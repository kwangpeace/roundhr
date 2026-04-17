FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cron 서비스가 컨테이너를 띄울 때마다 1회 실행 (Railway 대시보드에서 스케줄 지정)
CMD ["python", "-m", "src.main"]
