#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim-2024-07-15
FROM python:3.11.9-slim


RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN pip install -U pip &&\
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1


#WORKDIR /app
#ENV PYTHONPATH=/app
#ENV PYTHONDONTWRITEBYTECODE=1

# First copy only requirements.txt to cache dependencies independently
#COPY requirements.txt /app
#RUN pip install --no-cache-dir -r requirements.txt



#ENV UVICORN_HOST=0.0.0.0 UVICORN_PORT=80 UVICORN_LOG_LEVEL=info
