#!/bin/bash

set -e

# wait for rabbitmq to start
while !</dev/tcp/rabbitmq/${RABBIT_PORT}; do
  sleep 5
done

python manage.py rundramatiq
