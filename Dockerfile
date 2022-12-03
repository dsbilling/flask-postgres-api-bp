
FROM tiangolo/uwsgi-nginx-flask:python3.9

RUN apt-get update -qq \
  && DEBIAN_FRONTEND=noninteractive apt-get install -yq \
    libpq-dev \
    gcc

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt