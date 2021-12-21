#!/bin/bash

set -e

if [[ "$1" == "off" ]]; then
    rfkill block bluetooth
    exit 0
fi

device_name="$1"

if [[ -z "$device_name" ]]; then
    echo "Usage: $0 <device_name>"
fi

# turn on bluetooth
rfkill unblock bluetooth


# Get MAC address
mac_address=""

for nb_attempt in $(seq 1 10); do
    mac_address=$(bt-device -l 2> /dev/null | grep -i "$device_name" | perl -pe 's@.+\((.+)\)@\1@')
    if [[ -n "$mac_address" ]]; then
        break
    fi
    sleep 0.5
done
echo -e "connect $mac_address" | bluetoothctl 2> /dev/null | grep connect
