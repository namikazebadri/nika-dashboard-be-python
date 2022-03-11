FROM python:3.8.10-alpine3.13

RUN mkdir -p /home/app

RUN addgroup -S app && adduser -S app -G app

ENV DJANGO_HOME=/home/app

RUN mkdir -p $DJANGO_HOME

WORKDIR $DJANGO_HOME

RUN apk update && apk add --virtual \
    build-deps \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libcurl \
    curl-dev \
    libmagic

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

RUN pip install pipenv
RUN pip install pytest

COPY ./Pipfile Pipfile
COPY ./Pipfile.lock Pipfile.lock

RUN pipenv install --system

USER app

ADD --chown=app:app . $DJANGO_HOME

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:8000 app.wsgi