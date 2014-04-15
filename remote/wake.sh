#!/bin/bash

# USAGE ./wake.sh <host> <deploy_id>

set -e

if [ -z $1 ]; then
    echo "Please provide host as the first argument"
    exit 1
fi
if [ -z $2 ]; then
    echo "Please provide deployment id as the second argument"
    exit 1
fi

HOST=$1
DEPID=$2
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "
bash container/wake.sh $DEPID
bash container/prox.sh $DEPID
" | ssh -i $DIR/../pk.pem deployer@"$HOST" 'cd deploy && bash -s'
