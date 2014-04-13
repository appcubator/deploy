#!/bin/bash
set -e
# Usage:
#   proxy <deploy id> <domain> <port>
#   proxy <deploy id> --sleep
# Examples:
#   proxy molten-yearling molten-yearling.appcbtr.com 43534
#   proxy molten-yearling "*.molten-yearling.appcbtr.com" 43534
#   proxy molten-yearling --sleep

REDIS_HOST=10.204.203.78
DEPID=$1
SLEEPFLAG=$2

if [ "$#" = "2" ]; then
    if [ "$SLEEPFLAG" != "--sleep" ]; then
        echo "What the heck is $SLEEPFLAG ? Did you mean --sleep ?"
        exit 1
    fi
    curl "http://$REDIS_HOST:7379/SET/sleeping:$DEPID/1"
    exit 0
fi

DOMAIN=$2
IP=$(ifconfig eth0 | sed -n 2p | cut -d ":" -f2 | cut -d " " -f10)
PORT=$3

curl "http://$REDIS_HOST:7379/SET/sleeping:$DEPID/0"
curl "http://$REDIS_HOST:7379/DEL/frontend:$DOMAIN"
curl "http://$REDIS_HOST:7379/RPUSH/frontend:$DOMAIN/$DEPID"
curl "http://$REDIS_HOST:7379/RPUSH/frontend:$DOMAIN/http%3A%2F%2F$IP:$PORT"
