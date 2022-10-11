#!/bin/bash
set -e

if [[ "$1" == "quick" ]]; then
    mbsync -V inria:INBOX outlook:INBOX gmx:INBOX ymail:INBOX > /tmp/mbsync-quick.log 2>&1
else
    mbsync -a -V > /tmp/mbsync.log 2>&1
fi

# mu server is started by mu4e. If it exists mu index can not start with a
# "Unable to get write lock". Adapted from
# https://github.com/djcb/mu/issues/8#issuecomment-396649525
if pgrep -f 'mu server'; then
    echo "mu is already running, going through emacs" >> /tmp/mbsync.log
    emacsclient -e '(mu4e-update-index)' >> /tmp/mbsync.log 2>&1
else
    echo "mu is not running, indexing mail database" >> /tmp/mbsync.log
    mu index --maildir=~/.mail >> /tmp/mbsync.log 2>&1
fi
