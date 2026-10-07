#!/bin/bash

screen=eDP-1
args=$(xrandr --query | awk -v s="$screen" '$1==s {print /[0-9]+x[0-9]+[+-][0-9]+[+-][0-9]+/ ? "--off" : "--auto"}')

xrandr --output "$screen" "$args"
