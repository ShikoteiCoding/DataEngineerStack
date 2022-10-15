#!/usr/bin/env bash
CONTROL_NODE="data-engineer-k3s"

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

InitVM() {
    echo "Initializing the VM..."
    echo "Updating apt package, installing..."
    multipass exec $CONTROL_NODE sudo apt-get update
    multipass exec $CONTROL_NODE sudo apt-get upgrade
    echo "Rebooting the virtual machine to apply changes..."
    multipass stop $CONTROL_NODE
    sleep 10    # Avoid multipass conflicts
    multipass start $CONTROL_NODE
    echo "Installing k3s package ..."
    multipass exec $CONTROL_NODE -- curl -L https://get.k3s.io > ~/k3s-install.sh
    multipass exec $CONTROL_NODE -- sh ~/k3s-install.sh
}

if ! $(multipass list | grep -q $CONTROL_NODE); then
    echo "The control plane VM does not exit ... Creating it..."
    multipass launch --name $CONTROL_NODE --cpus 2 --mem 2048M --disk 10G focal
    InitVM
else
    echo "The control plane VM is found ... Starting it..."
    multipass start $CONTROL_NODE
fi