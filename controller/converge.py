#!/usr/bin/env python

# input the files
#   list of container, host pairs

# for each remote host:
#   remote get list of containers

# diff the target state with the current state to output a list of actions
#   to_create = target_containers - remote_containers
#   to_delete = remote_containers - target_containers

# execute the actions using ssh
#   for each remote host:
#     call remote bulk_create shell script, pass to_create containers to stdin.
#     call remote bulk_delete shell script, pass to_delete containers to stdin.

from models import Machine, Container


machines = Machine.load_state() # machine name => machine
containers = Container.load_state() # deploy id => container

print containers
