# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY tests/tests-requirements.txt tests-requirements.txt

RUN apt-get update && \
    apt-get install -y poppler-utils

RUN pip install -r tests-requirements.txt
COPY . .