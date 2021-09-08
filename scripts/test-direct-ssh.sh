#!/bin/bash

hostname=$1
port=${2:-22}
# echo hostname: $hostname
# echo port: $port

timeout 0.2 bash -c "</dev/tcp/$hostname/$port"

exit_code=$?
# echo exit_code: $exit_code

if [ $exit_code -eq 0 ]; then
    echo "direct SSH to $hostname succeeded"
else
    echo "direct SSH to $hostname failed"
fi

exit $exit_code
