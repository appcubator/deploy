#!/bin/bash
set -e
# Usage: ./get_port.sh molten-yearling

DEPID=$1

# echo "Polling docker for the port"
COUNTER=1
PORT_OUT=''
while [ 1 ]; do
    # echo "The counter is $COUNTER"

    set +e
    PORT_OUT=$(/usr/bin/docker port devmon-$DEPID 5000 2> /dev/null)
    set -e

    if [[ "$?" -ne "0" ]]; then
        # echo "Trying again, docker error: $PORT_OUT"
        continue
    fi

    PORT=$(echo $PORT_OUT | sed 's/.*:\([:digit:]*\)/\1/')

    if [[ "$PORT" -ne "" ]]; then
        break
    fi

    sleep 1
    let COUNTER=COUNTER+1
done

echo "$PORT"
