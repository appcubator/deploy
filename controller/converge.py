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

def converge(key='*'):
    # note that this gets the machines in the `key` cluster
    machines = Machine.load_files(key=key) # machine name => machine

    # note that this gets all containers accross all users.
    # we are converging the entire `key` machine group within the cluster
    containers = Container.load_files(machines) # deploy id => container

    print machines, containers

    threads = []
    for m in machines.values():
        target_containers = [c for c in containers.values() if c.machine == m]
        (to_create, to_delete, t1, t2) = m.converge(target_containers)
        threads.append(t1)
        threads.append(t2)

    for t in threads:
        t.join()

if __name__ == "__main__":
    converge()

