#!/bin/bash
alembic upgrade head

if [ "$FLASK_ENV" = "development" ]; then
    echo "Starting in development mode"
    python api.py
elif [ "$FLASK_ENV" = "test" ]; then
    echo "Starting Test Mode"
    pytest -v
else
    echo "Starting in production mode"
    gunicorn -w 4 -b 0.0.0.0:5000 api:api
fi