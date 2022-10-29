# Local Kubernetes Installation for Macos (sorry)

This readme is giving requirements and commands to install and build locally k3s and provided stack for macos. Deployment of k3s for ubuntu does not need multipass.

## Multipass for k3s

Install multipass for macos here: https://multipass.run/install

Macos:
```
brew update
brew install multipass
```

# Installation

For simplicity purpose we will deploy only one node with multiple pods inside. As this is a local deployment there is not specific need to complexify the stack with slave nodes.

## VM Build with k3s

### Manual build

Create a VM
```
multipass launch --name data-engineer-k3s --cpus 2 --mem 2048M --disk 5G focal
```

Start the VM
```
multipass start data-engineer-k3s
```

Upgrade apt inside the VM
```
multipass shell data-engineer-k3s
sudo apt-get update
sudo apt-get upgrade
```

Restart the VM and install k3s
```
multipass stop data-engineer-k3s
multipass start data-engineer-k3s
multipass shell data-engineer-k3s
curl -sfL https://get.k3s.io | sh -
```

Get the master node token and the IP:
```
sudo cat /var/lib/rancher/k3s/server/node-token
multipass list
```

### Automatic build

```
bash script.sh local-k3s 10
```

## Anexes

### Helper URLs
https://www.weave.works/blog/kafka-on-kubernetes-and-deploying-best-practice
https://github.com/superseb/multipass-k3s/blob/master/multipass-k3s.sh