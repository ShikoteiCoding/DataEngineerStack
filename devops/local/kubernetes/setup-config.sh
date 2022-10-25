#!/usr/bin/env bash

echo "Setup the k3s config..."

# Checking the kubeconfig
if ! echo $KUBECONFIG | grep -q "$HOME/.kube/config" ; then
    echo "KUBECONFIG=$HOME/.kube/config" > $PWD/variables.sh
    source $PWD/variables.sh
fi

# Creating the directory
if [ -d "$HOME/.kube" ]; then
    echo "$HOME/.kube already exists..."
else
    mkdir $HOME/.kube
fi

# Creating the config file
if [ -f "$HOME/.kube/config" ]; then
    echo "$HOME/.kube/config already exists..."
else 
    sudo chmod 777 /etc/rancher/k3s/k3s.yaml
    mv /etc/rancher/k3s/k3s.yaml $HOME/.kube/config
fi

sed -i 's/default/atna/g' $HOME/.kube/config    # Make sure the name is atna
sudo chown -R $(id -u):$(id -g) $HOME/.kube/    # Unlock kubectl auto config locking

echo "Using atna as a kubectl context..."
kubectl config use-context atna