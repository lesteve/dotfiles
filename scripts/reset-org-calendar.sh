#!/bin/bash

for f in ~/org/org-caldav-*.el ~/org/zimbra-*.org ~/org/org-caldav-backup.org; do
    mv $f $f.bak
done


