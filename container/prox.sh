#!/bin/bash
set -e
# Examples:
#   ./proxy.sh molten-yearling
#   ./proxy.sh molten-yearling --sleep

DEPID=$1
SLEEPFLAG=$2
WAIT=false
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "$DEPID" ]; then
    echo "First arg is deployment id"
    exit 1
fi

if [ -n "$SLEEPFLAG" ]; then
    if [ "$SLEEPFLAG" != "--sleep" ]; then
        if [ "$SLEEPFLAG" != "--wait" ]; then
            echo "What the heck is $SLEEPFLAG ? Did you mean --sleep or --wait?"
            exit 1
        else
            WAIT=true
        fi
    else
        $DIR/../proxy.sh $DEPID --sleep
        exit 0
    fi
fi

echo "Polling docker for the port"
PORT=$(sh $DIR/get_port.sh $DEPID)

sh $DIR/../proxy.sh $DEPID "$DEPID.appcbtr.com" "$PORT"
sh $DIR/../proxy.sh $DEPID "*.$DEPID.appcbtr.com" "$PORT"

# WAIT till devmon is up so we can POST a tar of the updated code.
# TODO FIXME this could potentially go on forever...
if $WAIT; then
    # the Host header tricks it to go to devmon
    until $(curl --output /dev/null --header "Host: devmon.whatever.com" --silent --head --fail http://127.0.0.1:$PORT); do
        sleep 0.75
    done
fi
