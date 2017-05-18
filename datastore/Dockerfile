FROM python:3-alpine

RUN pip install \
 flask \
 flask-restplus \
 SQLAlchemy

ADD . /app
ENV PYTHONPATH /app
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["python", "-m", "app.datastore"]
