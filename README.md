# PDF-rendering-service

Service for rendering PNG images from PDF files

## Deployment

- ensure env variables stored in `.env` are correct
- RabbitMQ port is set in `docker_conf/rabbitmq.conf`
- start app with `docker-compose up` command in project root directory

## REST API Endpoints

- POST /api/documents/
    - uploads a file
    - returns JSON { “id”: “<DOCUMENT_ID>? }
- GET /api/documents/<DOCUMENT_ID>
    - returns JSON { “status”: “processing|done”, “n_pages”: NUMBER }
- GET /api/documents/<DOCUMENT_ID>/pages/<NUMBER>
    - returns rendered image png
  
## Tests
  
- Tests location `pdf_rendering_service/service_app/tests.py`
- Run tests from `tests` folder with:
    - `docker-compose up --build --exit-code-from test-web`
