#!/bin/bash

# For now this is not a build file. Just used it to store commands
multipass launch — name collector-node — cpus 1 — mem 128M — disk 1G focal

multipass exec collector-node sudo apt update
multipass exec collector-node sudo apt upgrade
multipass exec collector-node curl -sfL https://get.k3s.io | K3S_URL=https://192.168.64.3:6443 K3S_TOKEN=K10db85acbbade8b2e7df2057aa8c51eaf60964fe2703c174064df0b0b6becb8d87::server:eb6d552feec9d8fd9b28ca70d206c1a2 sh -
multipass exec kubectl apply -f collector-deployment.yaml
multipass exec kubectl apply -f collector-service.yaml