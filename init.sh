#!/bin/sh
LIMIT=3
HOST=23.20.221.191

for i in `tail -n 109 hostnames.txt`; do
echo "
bash container/create.sh $i
bash container/prox.sh $i
bash container/sleep.sh $i
bash container/prox.sh $i --sleep
"
done | ssh -i pk.pem deployer@"$HOST" 'cd deploy && bash -s'
