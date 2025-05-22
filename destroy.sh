#!/bin/bash
echo "[1/3] Stopping and removing ml-model container..."
docker stop ml-model && docker rm ml-model

echo "[2/3] Stopping and removing Prometheus container..."
docker stop prometheus && docker rm prometheus

echo "[3/3] Stopping and removing Grafana container..."
docker stop grafana && docker rm grafana

echo "All services stopped and cleaned up."