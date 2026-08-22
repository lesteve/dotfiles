#!/bin/bash
set -e
set -o pipefail

log_file=/tmp/mbsync.log

# Add missing headers in GMX Inbox new folder. For now missing Date header only
# happens for GUM emails.
# If one day this is too slow (I doubt it) you could do something like this:
# files=$(rg --files-without-match -U -i '^Date:' ~/.mail/gmx/Inbox/new)
# python ~/scripts/add-missing-date-header-to-email.py ${=files}
python ~/scripts/add-missing-date-header-to-email.py ~/.mail/gmx/Inbox/new 2>&1 | tee $log_file

mbsync -V -a 2>&1 | tee -a $log_file || echo "mbsync issue"

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
