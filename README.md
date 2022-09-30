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
We might add an orchestrater to simulate more complex deployments (Kubernetes ?).

## Local Installation

### Kubernetes / Minikube

Macos:
```
brew update
brew install hyperkit
brew install minikube

brew install multipass
```

## Start

### Minikube

As we are full local for now, we start with a minikube local nodes. Remember, with Minikube the master nodes and kubernetes nodes are all running in a local VM. Usually it is not the case.

Starting a minikube VM:
```
minikube start --vm-driver=hyperkit
```

Stopping a minikube VM:
```
minikube stop
```

### K3S

#### Creating the master (control-plane) node:

Create the node from host machine:
```
multipass launch --name control-plane-k3s --cpus 2 --nem 2058M --disk 5G focal
```

Start the node if already created:
```
multipass start
```

Login to the node:
```
multipass shell control-plane-k3s
```

Inside the VM, install K3S:
```
sudo apt update
sudo apt upgrade
curl -sfL https://get.k3s.io | sh -
```

Get the master node token and the IP:
```
sudo cat /var/lib/rancher/k3s/server/node-token
multipass list
```

#### Creating child node

Create the node from host machine:
```
multipass launch — name child-node-name — cpus 2 — mem 2048M — disk 5G focal
```

Login to the node (replace the name):
```
multipass shell child-node-name
```

Inside the node, install k3s and link the child node to the master node (with above mentionned token and ip address):
```
sudo apt update
sudo apt upgrade
curl -sfL https://get.k3s.io | K3S_URL=https://master-node-ip:6443 K3S_TOKEN=master-node-token sh -
```

List the child nodes from the master node (log inside):
```
sudo kubectl get node -o wide
```