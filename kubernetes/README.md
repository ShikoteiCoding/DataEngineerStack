# Local Kubernetes Installation

## K3S

Macos:
```
brew update
brew install multipass
```

# Start

## Creating the master node (control-plane) :

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

## Creating a child node

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