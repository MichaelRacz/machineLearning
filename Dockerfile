FROM python:3-alpine

RUN apk add --no-cache musl-dev gcc

RUN pip install \
 flask \
 flask-restplus \
 SQLAlchemy \
 pykafka

ADD . /app
ENV PYTHONPATH /app
ENV DATASTORE_SETTINGS /app/docker-compose.prod.yml
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["python", "-m", "app.datastore"]
