#!/bin/sh
LIMIT=3
HOST=23.20.221.191

for i in `head -n "$LIMIT" hostnames.txt`; do
echo "
cd deploy
bash container/create.sh $i
bash container/sleep.sh $i
bash container/prox.sh $i --sleep
sleep 3
"
done | ssh -i pk.pem deployer@"$HOST" 'bash -s'
