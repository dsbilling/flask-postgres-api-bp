#ARG PYTHON_VERSION=3.9

#FROM python:$PYTHON_VERSION-slim-buster

FROM tiangolo/uwsgi-nginx-flask:python3.9

RUN apt-get update -qq \
  && DEBIAN_FRONTEND=noninteractive apt-get install -yq \
    libpq-dev \
    gcc

WORKDIR /app

COPY . /app

RUN pip install -r ./requirements.txt