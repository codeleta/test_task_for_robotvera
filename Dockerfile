FROM python:3.6.5-alpine3.7

LABEL maintainer="rouk@inbox.ru"
LABEL vendor="demidenkoya"

ENV LIBRARY_PATH=/lib:/usr/lib \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100


# System deps:

RUN apk update \
    && apk --no-cache add \
      bash \
      build-base \
      curl \
      gcc \
      gettext \
      git \
      libffi-dev \
      linux-headers \
      musl-dev \
      postgresql-dev \
      tini \
      jpeg-dev \
      zlib-dev \
      tzdata
ENV TZ "Europe/Moscow"

# Creating folders, and files for a project:

WORKDIR /code
COPY . /code

# Project initialization:

RUN pip install -r requirements.txt
