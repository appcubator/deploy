#!/bin/sh
HOST=23.20.221.191

git archive --format tar master | ssh -i pk.pem deployer@"$HOST" 'tar xf -'
