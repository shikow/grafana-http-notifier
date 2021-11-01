FROM python:3.8-slim

EXPOSE 5000

WORKDIR /app

RUN pip install --upgrade pip && pip --no-cache-dir install poetry

COPY  pyproject.toml .

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY app.py .

COPY dynamo.py .

COPY sqs.py .

ENTRYPOINT poetry run gunicorn --workers 2 --bind 0.0.0.0:5000 app:app