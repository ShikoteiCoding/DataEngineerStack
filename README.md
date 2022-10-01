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