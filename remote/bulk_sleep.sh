#!/bin/bash

HOST=$1

for i in `cat -`; do
echo "
bash container/sleep.sh $i
bash container/prox.sh $i --sleep
"
done | ssh -i pk.pem deployer@"$HOST" 'cd deploy && bash -s'
