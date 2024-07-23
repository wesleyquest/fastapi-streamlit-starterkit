FROM python:3.11-slim


RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

COPY . /app

RUN pip install -U pip &&\
    pip install --no-cache-dir -r requirements.txt

