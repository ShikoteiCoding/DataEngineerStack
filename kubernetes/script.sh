#!/usr/bin/env bash
CONTROL_PLANE_TOKEN="" # Master node token

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
echo $MULTIPASSCMD

if [ -n "$MERGE_KUBECONFIG" ]; then
    if [ -z "$KUBECONFIG" ]; then
        echo "Environment variable KUBECONFIG is empty, can't merge kubeconfig"
        exit 1
    fi
fi

if [ -z $CONTROL_PLANE_TOKEN ]; then
    CONTROL_PLANE_TOKEN=$(cat /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | fold -w 20 | head -n 1 | tr '[:upper:]' '[:lower:]')
    echo "No server token given, generated server token: ${CONTROL_PLANE_TOKEN}"
fi