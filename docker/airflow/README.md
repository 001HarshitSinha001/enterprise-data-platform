# Airflow Local Development

This folder contains a local Docker Compose setup for Apache Airflow.

## Start Airflow

From `docker/airflow` run:

```bash
docker-compose up -d
```

## Access

- Airflow webserver: http://localhost:8080

## Notes

- DAGs are mounted from the project root into `/opt/airflow`
- Place DAG files inside `airflow_dags/dags`
- The Airflow image is configured with PostgreSQL and Redis
