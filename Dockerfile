FROM python:3.6.1-alpine

ADD . /app
WORKDIR /app

RUN apk add --no-cache musl-dev gcc
RUN pip install -r requirements.txt

ENV PYTHONPATH /app
ENV CONFIG_FILE /app/config.prod.py
EXPOSE 80
ENTRYPOINT ["python", "-m", "app.datastore"]
