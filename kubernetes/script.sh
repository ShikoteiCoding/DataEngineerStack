#!/usr/bin/env bash
CONTROL_PLANE_TOKEN="K10db85acbbade8b2e7df2057aa8c51eaf60964fe2703c174064df0b0b6becb8d87::server:eb6d552feec9d8fd9b28ca70d206c1a2" # Master node token

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

# Start the collector node
multipass start collector-node
while [[ $(multipass exec collector-node sudo kubectl get nodes  --no-header 2>/dev/null | grep -c -v "not found") ]];
do 
    echo "Waiting for collector-node to start...";
    sleep 2; 
done

# Start the bropker node
multipass start broker-node
while [[ $(multipass exec broker-node sudo kubectl get nodes  --no-header 2>/dev/null | grep -c -v "not found") ]];
do 
    echo "Waiting for broker-node to start...";
    sleep 2; 
done