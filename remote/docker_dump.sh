#!/bin/bash

# USAGE ./docker_dump.sh <host>

set -e

if [ -z $1 ]; then
    echo "Please provide host as the first argument"
    exit 1
fi

HOST=$1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ssh -i $DIR/../pk.pem deployer@"$HOST" 'docker inspect `docker ps -aq | xargs`'
