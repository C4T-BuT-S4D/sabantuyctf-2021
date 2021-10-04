FROM python:3.8-alpine

RUN adduser -s /bin/false -D -H service

WORKDIR /var/service

COPY service/requirements.txt .

RUN pip install -r requirements.txt

COPY service .

USER service

ENTRYPOINT hypercorn --workers 4 --bind 0.0.0.0:8000 server:app
