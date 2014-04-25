#!/bin/sh
HOST=$1

git archive --format tar master | ssh -i pk.pem deployer@"$HOST" 'mkdir -p deploy && cd deploy && tar xf -'
