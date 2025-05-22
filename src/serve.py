from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import joblib
import pandas as pd
import uvicorn

import prometheus_client
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI()
model = joblib.load("model.pkl")

# Define empty placeholders
REQUEST_COUNT = None
REQUEST_LATENCY = None

@app.on_event("startup")
def setup_metrics():
    global REQUEST_COUNT, REQUEST_LATENCY
    try:
        REQUEST_COUNT = Counter("prediction_requests", "Number of prediction requests")
    except ValueError:
        REQUEST_COUNT = prometheus_client.REGISTRY._names_to_collectors["prediction_requests"]

    try:
        REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency")
    except ValueError:
        REQUEST_LATENCY = prometheus_client.REGISTRY._names_to_collectors["request_latency_seconds"]

@app.post("/predict")
async def predict(request: Request):
    if REQUEST_LATENCY and REQUEST_COUNT:
        REQUEST_COUNT.inc()

    payload = await request.json()
    data = pd.DataFrame([payload])

    with REQUEST_LATENCY.time() if REQUEST_LATENCY else nullcontext():
        prediction = model.predict(data)

    return {"prediction": int(prediction[0])}

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest())

# Context manager fallback for latency tracking
from contextlib import nullcontext

if __name__ == "__main__":
    uvicorn.run("serve:app", host="0.0.0.0", port=8000)
