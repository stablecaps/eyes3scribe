#!/bin/bash

set -e

MYREPO=$1
DEEPSOURCE_DSN=$2

if [ -z "$MYREPO" ] || [ -z "$DEEPSOURCE_DSN" ] ; then
    echo "Please provide correct arguments"
    exit 1
fi

source ${HOME}/.ssh/github_pat_token.txt

python3 _make/upload_repo_secret.py \
    --token $GITHUB_AUTH_TOKEN \
    --repository ${MYREPO} \
    --secret_name GHRS_GITHUB_API_TOKEN \
    --secret_value ${GITHUB_SECRET} \
    --owner "stablecaps"

python3 _make/upload_repo_secret.py \
    --token $GITHUB_AUTH_TOKEN \
    --repository ${MYREPO} \
    --secret_name DEEPSOURCE_DSN_SECRET \
    --secret_value ${DEEPSOURCE_DSN} \
    --owner "stablecaps"
