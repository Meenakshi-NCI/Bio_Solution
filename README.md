> [!IMPORTANT]  
> This is a DevOps interview exercise for BioSimulytics Limited. Please do not share your solution publicly.

# DevOps Interview Exercise
Our [weather prediction microservice](https://github.com/orgs/BioSimulytics-Limited/packages/container/package/dummy-weather-api) **keeps crashing in production** and killing its container. We're seeing it in the logs, but we don't know why! Documentation for the service can be found in [WEATHER_API_DOCS.md](WEATHER_API_DOCS.md).

## Running the Service
**Requirements:** Docker, Docker Compose v2, Python 3.10+

We've provided the production `docker-compose.yml` file that will run the service locally and a python script `test_endpoint.py` that will hit the service with a load of requests.

## Deliverables
Your job is to build an observability/monitoring service that can help us understand why our microservice is crashing. You can use any tools you want. The service should capture memory usage, CPU usage, network usage, restart/failover history and logs. 

Using the monitoring data, figure out the root cause of the crash and explain it in a brief paragraph.