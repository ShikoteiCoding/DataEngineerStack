#!/usr/bin/env bash
CONTROL_PLANE_TOKEN="K10db85acbbade8b2e7df2057aa8c51eaf60964fe2703c174064df0b0b6becb8d87::server:eb6d552feec9d8fd9b28ca70d206c1a2" # Master node token
CONTROL_NODE="control-plane-k3s"

# Check multipass binary
if [ -x "$(command -v multipass.exe)" > /dev/null 2>&1 ]; then
    # Windows
    MULTIPASSCMD="multipass.exe"
elif [ -x "$(command -v multipass)" > /dev/null 2>&1 ]; then
    # Linux/MacOS
    MULTIPASSCMD="multipass"
else
    echo "The multipass binary (multipass or multipass.exe) is not available or not in your \$PATH"
    exit 1
fi

if ! $(multipass list | grep -q $CONTROL_NODE) ; then
    echo "The control plane VM does not exit ... Creating it..."
    multipass launch --name $CONTROL_NODE --cpus 2 --mem 2048M --disk 5G focal
else
    echo "The control plane VM is found ..."
fi

echo "Launching the control plane VM ..."
multipass start $CONTROL_NODE

#while [[ $(multipass exec $CONTROL_NODE sudo kubectl get nodes  --no-header 2>/dev/null | grep -c -v "not found") ]];
#do 
#    echo "Waiting for $CONTROL_NODE to start..."
#    sleep 2;
#done

#while [[ $(multipass list | grep control-plane-k3s | awk '{print $2}' | grep -q 'Stopped') ]]; 
#do
#    echo "Waiting for $CONTROL_NODE to start..."
#    sleep 5
#done

if ! $(multipass exec control-plane-k3s echo "$(command -v apt)" | grep -q 'apt'); then
    echo "Missing apt package, installing..."
    multipass exec $CONTROL_NODE sudo apt update
    multipass exec $CONTROL_NODE sudo apt upgrade
else
    echo "apt package already installed..."
fi

if ! $(multipass exec control-plane-k3s echo "$(command -v kubectl)" | grep -q 'kubectl'); then
    echo "Missing k3s package, installing..."
    multipass exec $CONTROL_NODE sudo curl -sfL https://get.k3s.io | sh -
else
    echo "k3s package already installed..."
fi