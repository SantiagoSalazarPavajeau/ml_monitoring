FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install fastapi uvicorn scikit-learn pandas joblib prometheus_client
EXPOSE 8000
CMD ["python", "src/serve.py"]
