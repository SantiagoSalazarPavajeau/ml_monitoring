#!/bin/bash
echo "[1/4] Building Docker image..."
docker build -t ml-model-server .

echo "[2/4] Starting ML model container..."
docker run -d --name ml-model -p 8000:8000 ml-model-server

echo "[3/4] Starting Prometheus..."
docker run -d --name prometheus -p 9090:9090 \
  -v $(pwd)/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

echo "[4/4] Starting Grafana..."
docker run -d --name=grafana -p 3000:3000 grafana/grafana

echo "All services running. FastAPI on 8000, Prometheus on 9090, Grafana on 3000."
