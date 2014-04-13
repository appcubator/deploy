#!/bin/sh

# USAGE ./create.sh <deploy_id>

set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z $1 ]; then
    echo "Please provide deployment id as the first argument"
    exit 1
fi

DEPID=$1

/usr/bin/docker stop devmon-$DEPID
$DIR/prox.sh $DEPID --sleep
