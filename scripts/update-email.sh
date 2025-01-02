#!/bin/bash
set -e
set -o pipefail

log_file=/tmp/mbsync.log

if [[ "$1" == "quick" ]]; then
    args="inria:INBOX outlook:INBOX gmx:INBOX ymail:INBOX"
else
    args="-a"
fi

mbsync -V $args 2>&1 | tee /tmp/mbsync.log || echo "mbsync issue"

# mu server is started by mu4e. If it exists mu index can not start with a
# "Unable to get write lock". Adapted from
# https://github.com/djcb/mu/issues/8#issuecomment-396649525
if pgrep -f 'mu server'; then
    echo "mu is already running, going through emacs" | tee -a "$log_file"
    emacsclient -e '(mu4e-update-index)' 2>&1 | tee -a "$log_file"
else
    echo "mu is not running, indexing mail database" | tee -a "$log_file"
    mu index 2>&1 | tee -a "$log_file"
fi
