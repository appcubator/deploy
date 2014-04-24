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

machines = Machine.load_state('prod') # machine name => machine
containers = Container.load_state(machines, 'prod') # deploy id => container

from threading import Thread
threads = []

for m in machines.values():
    remote_containers = Container.load_remote_state(m)

    to_create = set(containers) - set(remote_containers)
    t = Thread(target=m.bulk_create, args=(to_create,))
    t.start()
    threads.append(t)

    to_delete = set(remote_containers) - set(containers)
    t = Thread(target=m.bulk_destroy, args=(to_delete,))
    t.start()
    threads.append(t)

for t in threads:
    t.wait()

print containers

