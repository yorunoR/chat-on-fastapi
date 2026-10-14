FROM python:3.13-bookworm

ENV LANG=C.UTF-8 TZ=Asia/Tokyo PYTHONPATH=.

WORKDIR /api

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --upgrade pip \
    && pip install uv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
