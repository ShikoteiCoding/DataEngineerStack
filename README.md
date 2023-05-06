# DataEngineerStack
Model data stack tools to showcase some basics.

Demonstrate a simple data stack and implements some additional features to play with.
Built upon event-driven architecture. Should be what modern companies use if they have access to DevOps and Data Engineer resources.

Not tight to any cloud provider, easy to migrate and maintain.

## Global Stack

For now the stack is local docker containers. K8S is in the roadmap.

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

## Batch Jobs
```
+------------+          +----------+        +----------+
|            |  csv     | Pyspark  |   SQL  |          | 
| Data Loader| +------->|   Jobs   | +----> | Postgres |
|            |          |          |        |          |
+------------+          +----------+        +----------+
```

## Streaming Jobs

```
+------------+           +-----------+           +----------+           +----------+        +----------+
|            |  JSON     |           |  JSON     |          |  JSON     | Pyspark  |   SQL  |          | 
| Data Faker | +-------> |  Logstash | +-------> |  Kafka   | +-------> |   Stream | +----> | Postgres |
|            |           |           |           |          |           |          |        |          |
+------------+           +-----------+           +----------+           +----------+        +----------+
```

## Twitter Batch Jobs

Simple usecase to show batch jobs with twitter data

### Build

```sh
docker compose build
```

### Run Loader Service

Run download container
```sh
docker compose up -d loader
```

### Run Spark Jobs

Run spark container
```sh
docker compose up -d spark --build
```

Execute a job
```sh
docker compose exec spark bin/spark-submit jobs/twitter/job_twitter_data_1.py
docker compose exec spark bin/spark-submit jobs/twitter/job_twitter_data_2.py
docker compose exec spark bin/spark-submit jobs/twitter/job_twitter_data_3.py
```

### Test

#### Test commons

Common part is a library helping the code architecture of actual jobs.
```sh
docker compose exec spark python3 -m pytest "tests/commons/test_commons.py" -p no:warnings --cov="jobs" -vv
```

#### Test actual job functions
WORKDIR is set to /opt/spark
```sh
docker compose exec spark python3 -m pytest "tests/twitter/test_job_twitter_data_1.py" -p no:warnings --cov="jobs" -vv
docker compose exec spark python3 -m pytest "tests/twitter/test_job_twitter_data_2.py" -p no:warnings --cov="jobs" -vv
docker compose exec spark python3 -m pytest "tests/twitter/test_job_twitter_data_3.py" -p no:warnings --cov="jobs" -vv
```