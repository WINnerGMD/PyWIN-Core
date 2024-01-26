#!/bin/bash

#
#alembic upgrade head
#alembic revision --autogenerate -m "Database creation"

gunicorn core:fastapi --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

