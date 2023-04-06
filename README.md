# DataEngineerStack
Model data stack tools to showcase some basics.

Demonstrate a simple data stack and implements some additional features to play with.
Built upon event-driven architecture. Should be what modern companies use if they have access to DevOps and Data Engineer resources.

Not tight to any cloud provider, easy to migrate and maintain.

## Stack

### Components

```
+-----------+           +----------+        +----------+        +----------+
|           |  measures |          |        |          |        | Serve    |  metrics
| Telemetry | +-------> |  Collect | +----> | Compute  | +----> |     Stats| +---->
|           |           |          |        |          |        |          |
+-----------+           +----------+        +----------+        +----------+
```

As we don't have any telemetry but we still wan't to play with some data, we will create a data generator and try to make it work from a config file.

### Design

```
+------------+           +-----------+           +----------+           +----------+        +----------+
|            |  JSON     |           |  JSON     |          |  JSON     | Pyspark  |   SQL  |          | 
| Data Faker | +-------> |  Logstash | +-------> |  Kafka   | +-------> |   Stream | +----> | Postgres |
|            |           |           |           |          |           |          |        |          |
+------------+           +-----------+           +----------+           +----------+        +----------+
```

Some additionnal tools are easy to plug, kafka and pyspark are very versatile.

## Build

```sh
docker compose build
```

## Run Loader Service

Run download container
```sh
docker compose up -d loader
```

## Run Spark Jobs

Run spark container
```sh
docker compose up -d spark --build
```

Execute a job
```sh
docker compose exec spark bin/spark-submit jobs/twitter/job_twitter_data_1.py
```

## Test

WORKDIR is set to /opt/spark
```sh
docker compose exec spark python3 -m pytest "tests/twitter/test_job_twitter_data_1.py" -p no:warnings --cov="jobs" -vv
```