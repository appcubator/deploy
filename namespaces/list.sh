#!/bin/bash

# USAGE ./list.sh <namespace>

set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z $1 ]; then
    echo "Please provide a valid namespace as the first argument"
    exit 1
fi

NAMESPACE=$1
cat "$DIR/$NAMESPACE.conf"
