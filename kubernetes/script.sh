#!/usr/bin/env bash
CONTROL_NODE=$1
RAM=$2

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

if [ -z "$RAM" ]; then
    echo "No RAM provided, choosing 5G."
    RAM="5G"
else
    RAM="${RAM}G"
fi

InitVM() {
    echo "Initializing the VM..."
    echo "Updating apt package, installing..."
    multipass exec $CONTROL_NODE -- sudo apt-get update
    multipass exec $CONTROL_NODE -- sudo apt-get upgrade

    echo "Rebooting the virtual machine to apply changes..."
    multipass stop $CONTROL_NODE
    sleep 10    # Avoid multipass conflicts
    multipass start $CONTROL_NODE
    sleep 5     # Avoid multipass conflicts

    echo "Transferring files from host to machine..."
    multipass transfer $PWD/build.sh $CONTROL_NODE:.
    multipass transfer $PWD/setup-config.sh $CONTROL_NODE:.
    multipass exec $CONTROL_NODE -- sudo chmod 777 build.sh
    multipass exec $CONTROL_NODE -- sudo chmod 777 setup-config.sh

    echo "Building k3s..."
    multipass exec $CONTROL_NODE -- sudo sh ./build.sh
}

if ! $(multipass list | grep -q $CONTROL_NODE); then
    echo "The control plane VM does not exit ... Creating it..."
    multipass launch --name $CONTROL_NODE --cpus 2 --mem 2048M --disk $RAM focal
    InitVM
else
    echo "The control plane VM is found ... Starting it..."
    multipass start $CONTROL_NODE
fi