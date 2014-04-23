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

class Machine(object):
  def __init__(self, name, host):
    self.name = name
    self.host = host

class Container(object):
  def __init__(self, d_id, machine):
    self.d_id = d_id
    self.machine = machine

machines = {}   # machine name => machine
containers = {} # deploy id => container


