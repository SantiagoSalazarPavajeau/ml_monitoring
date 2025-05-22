# Machine learning monitoring
A nimble docker deep learning project with monitoring set up (prometheus graphana)

To run we build the python FAST API learning model:

`docker build -t ml-model-server .`

Run the app on port 8080:

`docker run -d --name ml-model -p 8000:8000 ml-model-server`

Pull prometheus and grafana images:

```
docker pull prom/prometheus
docker pull grafana/grafana
```

Run prometheus (9090) and grafana (3000):

```
docker run -d --name prometheus -p 9090:9090 \           
  -v $(pwd)/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

docker run -d --name=grafana -p 3000:3000 grafana/grafana

```

Verify prometheus is scraping the app data by checking target health for ml-model Endpoint - http://host.docker.internal:8000/metrics

Create a grafana dashboard by adding prometheus as datasource: (http://host.docker.internal:9090) and adding queries for the desired metrics e.g.: rate(prediction_requests_total[1m])

Run the following shell in order to see a change in our graph data:
```
for i in {1..20}; do                 
  curl -s -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"Pclass": 1, "Age": 25, "Fare": 100, "Sex": 0}' > /dev/null
done
```

![Uploading Screenshot 2025-05-22 at 3.31.02 PM.png…]()


