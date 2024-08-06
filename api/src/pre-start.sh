#! /usr/bin/env bash

# Let the DB start
python ./src/backend_pre_start.py

# Run migrations
#alembic revision --autogenerate -m "message" # alembic.ini, env.py 수정하고 추가함. (초기에 한번만 실행하면 됨)
alembic upgrade head # 가장 상단의 버전으로 db가 upgrade됨 // alembic upgrade/downgrade revisionID # 해당 revision ID로 upgrade/downgrade

# Create initial data in DB
python ./src/initial_data.py
