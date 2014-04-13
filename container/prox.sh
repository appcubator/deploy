#!/bin/bash
set -e
# Examples:
#   ./proxy.sh molten-yearling
#   ./proxy.sh molten-yearling --sleep

DEPID=$1
SLEEPFLAG=$2
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "$DEPID" ]; then
    echo "First arg is deployment id"
    exit 1
fi

if [ -n "$SLEEPFLAG" ]; then
    if [ "$SLEEPFLAG" != "--sleep" ]; then
        echo "What the heck is $SLEEPFLAG ? Did you mean --sleep ?"
        exit 1
    fi
    $DIR/../proxy.sh $DEPID --sleep
    exit 0
fi

echo "Polling docker for the port"
PORT=$(sh $DIR/get_port.sh $DEPID)

sh $DIR/../proxy.sh $DEPID "$DEPID.appcbtr.com" "$PORT"
sh $DIR/../proxy.sh $DEPID "*.$DEPID.appcbtr.com" "$PORT"
