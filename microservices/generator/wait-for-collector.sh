#!/bin/sh
# wait-for-collector.sh

set -e
  
host="$1"
shift
  
until curl -d '{"body": "test"}' "http://$host:8080"; do
  >&2 echo "Collector is unavailable - sleeping"
  sleep 5
done
  
>&2 echo "Collector is up - executing command"