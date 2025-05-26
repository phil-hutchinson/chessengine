FROM python:3.11-slim

WORKDIR /app

# Install basic tools
RUN apt-get update && apt-get install -y \
    micro bash curl git \
    && rm -rf /var/lib/apt/lists/*

# Install Python debugger
RUN pip install --no-cache-dir debugpy

COPY . .
