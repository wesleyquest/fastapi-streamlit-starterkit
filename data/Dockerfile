FROM python:3.11.9-slim


RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

COPY . /app

RUN pip install -U pip &&\
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python","./src/chroma_data.py"]

#ENTRYPOINT ["streamlit", "run"]
#CMD ["main.py", "--server.port=$FRONTEND_SERVER_PORT"] --> DB 데이터 체크 만들기 
