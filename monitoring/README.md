# Components

## Prometheus

Prometheus is a metrics manager for monitoring purposes. 

Why ? It is a standard in all modern devops and data engineer toolstack. It has good integration with Grafana to visualise and a built-in alert manager for more operational monitoring.

## Grafana

Grafana is a dashboarding and exploring timeseries solutions.

Why ? It is light and variety of pluggins to integrate with other solutions (Loki for logs...). Grafana offer simple toolbox but can handle much more complexe data manipulation for specific needs. It also has an alert manager which can be useful for non technical people (UI helps people to create alerts).

# Run

```sh
docker compose -p stack-monitoring -f docker-compose.yml up -d
```

# UIs

Grafana: http://localhost:3000
Prometheus: http://localhost:9090