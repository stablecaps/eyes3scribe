#!/bin/bash

set -e

MYREPO=$1

if [ -z "$MYREPO" ]; then
    echo "Please provide correct arguments"
    exit 1
fi

source ${HOME}/.ssh/mod_github_settings.txt

python mod_github_settings.py -t $GH_MOD_TOKEN -r $MYREPO
