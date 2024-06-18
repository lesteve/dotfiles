#!/bin/bash

device_ids=$(
    xinput list \
        | grep -iP 'mouse|touchpad|trackpoint' \
        | perl -pe 's@.+id=(\d+).+@\1@')

for id in $device_ids; do
    xinput set-prop "$id" "libinput Left Handed Enabled" 1
done
