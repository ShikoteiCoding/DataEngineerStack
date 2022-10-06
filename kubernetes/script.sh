#!/usr/bin/env bash
CONTROL_PLANE_TOKEN="K10db85acbbade8b2e7df2057aa8c51eaf60964fe2703c174064df0b0b6becb8d87::server:eb6d552feec9d8fd9b28ca70d206c1a2" # Master node token
MASTER_NODE_NAME="control-plane-k3s"

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

if ! $(multipass list | grep -q $MASTER_NODE_NAME) ; then
    echo "The control plane VM does not exit ... Creating it..."
    multipass launch --name $MASTER_NODE_NAME --cpus 2 --mem 2048M --disk 5G focal
else
    echo "The control plane VM is found ..."
fi

echo "Launching the control plane VM ..."
multipass start $MASTER_NODE_NAME

while [[ $(multipass exec $MASTER_NODE_NAME sudo kubectl get nodes  --no-header 2>/dev/null | grep -c -v "not found") ]];
do 
    echo "Waiting for $MASTER_NODE_NAME to start..."
    sleep 2;
done