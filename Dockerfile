# TODO: Create docker file for each service

#FROM python:3.6.1-alpine
FROM frolvlad/alpine-python-machinelearning

ADD . /app
WORKDIR /app

#RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories
#RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories
#RUN apk update
#RUN apk add --no-cache libstdc++ lapack-dev && \
#    apk add --no-cache \
#        --virtual=.build-dependencies \
#        g++ gfortran musl-dev \
#        python3-dev
#
#RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# NOTE: Some packages from requirements.txt need musl-dev and gcc.
#   Check if these bugs are fixed in future versions and apk add can be avoided.
RUN apk add --no-cache musl-dev gcc python3-dev librdkafka

RUN ln -s /usr/bin/python3 /usr/bin/python

#RUN pip install numpy==1.12.1
#scipy==0.19.0
#scikit-learn==0.18.1

RUN pip3 install -r requirements.txt

ENV PYTHONPATH /app
ENV CONFIG_FILE /app/config.prod.py
EXPOSE 80
