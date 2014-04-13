#!/bin/sh

# USAGE ./create.sh <deploy_id>

set -e

if [ -z $1 ]; then
    echo "Please provide deployment id as the first argument"
    exit 1
fi

DEPID=$1

REGISTRY=10.204.203.78:5000
/usr/bin/docker run -d --name devmon-$DEPID -p 5000 $REGISTRY/devmon
prox.sh $DEPID
