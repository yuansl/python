#!/bin/bash

if [ -e /tmp/emacs$UID/server ];then
    exec emacsclient -n $@
else
    exec /usr/local/bin/em $@
fi
