FROM python:3.11.9-slim


ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install -U pip &&\
    pip install --no-cache-dir -r requirements.txt


#RUN chmod +x pre-start.sh && pre-start.sh

#DEV: fastapi dev ./src/main.py --host 0.0.0.0
#PROD: gunicorn src.main:app --bind 0:8000 --workers 2 --worker-class uvicorn.workers.UvicornWorker 

#ENV PYTHONPATH=/app
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV UVICORN_HOST=0.0.0.0 UVICORN_PORT=80 UVICORN_LOG_LEVEL=info
