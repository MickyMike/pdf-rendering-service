#!/bin/bash

set -e

# wait for postgresql to start
while !</dev/tcp/db/$POSTGRES_PORT; do
  sleep 5
done

# wait for rabbitmq to start
while !</dev/tcp/rabbitmq/${RABBIT_PORT}; do
  sleep 5
done

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
