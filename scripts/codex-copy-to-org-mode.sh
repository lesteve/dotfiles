#!/bin/bash
set -euo pipefail
echo pressed >> /tmp/pressed
xdotool key --clearmodifiers ctrl+o
sleep 0.3

markdown=$(xclip -selection clipboard -out)
org=$(printf '%s' "$markdown" |
    pandoc --from=gfm --to=org --wrap=none)
printf '%s' "$org" | xclip -selection clipboard -in
