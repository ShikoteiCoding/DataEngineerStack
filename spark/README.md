# Jobs

- Twitter jobs are used as exampel for proper development and testing features of common library

# Virtual env

## Requirements

- java8 for local spark on global python

## Installation
```sh
pip3 install -r requirements-spark.txt
pip3 install -r requirements-dev.txt
```

## Run

```sh
python3 spark_etls/twitter_jobs/job_twitter_data_1.py
python3 spark_etls/twitter_jobs/job_twitter_data_2.py
python3 spark_etls/twitter_jobs/job_twitter_data_3.py
```

# Docker

## Installation
```sh
docker build .
```

# k8s
soon