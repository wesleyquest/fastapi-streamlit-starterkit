FROM python:3.11.9-slim


RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

COPY . /app

RUN pip install -U pip &&\
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sh", "-c", "python ./src/rag/chroma_law_data.py && python ./src/gjf/main.py && python ./src/data_extraction_htc/main.py && python ./src/glossary_htc/main.py && python ./src/production_plan_htc/main.py"]

# ENTRYPOINT ["python", "./src/chroma_law_data.py"]
# ENTRYPOINT ["python", "./src/postgreSQL_gjf_data.py"]
#ENTRYPOINT ["streamlit", "run"]
#CMD ["main.py", "--server.port=$FRONTEND_SERVER_PORT"] --> DB 데이터 체크 만들기 
