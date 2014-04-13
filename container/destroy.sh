#!/bin/sh

# USAGE ./create.sh <deploy_id>

set -e

if [ -z $1 ]; then
    echo "Please provide deployment id as the first argument"
    exit 1
fi

DEPID=$1

/usr/bin/docker rm -f devmon-$DEPID
