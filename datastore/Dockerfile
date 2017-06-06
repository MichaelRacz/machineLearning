FROM python:3-alpine

RUN pip install \
 flask \
 flask-restplus \
 SQLAlchemy

ADD . /app
ENV PYTHONPATH /app
ENV DATASTORE_SETTINGS /app/docker-compose.prod.yml
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["python", "-m", "app.datastore"]
