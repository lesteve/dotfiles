#!/bin/bash
# matches=$(xdotool search --name emacs)

# echo $matches
# for match in $matches; do
#     echo "match: $match"
#     (xdotool windowactivate $match 2>&1 | grep failed) || break
# done

# Way simpler ...
wmctrl -a emacs
