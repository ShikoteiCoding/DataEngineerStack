# DataEngineerStack
Simple stack tools to showcase some basics.

Demonstrate a simple data stack and implements some additional features to play with.

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
+------------+           +----------+           +----------+           +----------+        +----------+
|            |  JSON     |          |  JSON     |          |  JSON     | Pyspark  |   SQL  |          | 
| Data Faker | +-------> |  Collect | +-------> |  Kafka   | +-------> |   Stream | +----> | Postgres |
|            |           |          |           |          |           |          |        |          |
+------------+           +----------+           +----------+           +----------+        +----------+
```

If needed we might add additional layers or forking of our pipeline which is yet quite simple. We might also want to deal with multiple pyspark streams through a kubernetes or any other container orchestrater.