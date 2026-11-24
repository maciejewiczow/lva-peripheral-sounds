FROM ghcr.io/astral-sh/uv:python3.14-bookworm

ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends pipewire-bin pulseaudio-utils 

COPY . /app
WORKDIR /app

RUN uv sync

CMD uv run main.py
