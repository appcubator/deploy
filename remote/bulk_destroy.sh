#!/bin/bash

# First arg should be host you're deleting containers on.
# Pass the deploy IDs into STDIN, separated by whitespace.

# Example:
#   echo "test4 test5 test6" | bash bulk_destroy 10.178.2.185

HOST=$1

for i in `cat -`; do
echo "
bash container/destroy.sh $i
#bash container/prox.sh $i
"
done | ssh -i pk.pem deployer@"$HOST" 'cd deploy && bash -s'
