#!/usr/bin/env python


from models import Machine, Container

def converge(key='*'):
    # note that this gets the machines in the `key` cluster
    machines = Machine.load_files(key=key) # machine name => machine

    # note that this gets all containers accross all users.
    # we are converging the entire `key` machine group within the cluster

    print machines, containers

    threads = []
    for m in machines.values():
        target_containers = [c for c in containers.values() if c.machine == m]
        (to_create, to_delete, t1, t2) = m.converge(target_containers)
        threads.append(t1)
        threads.append(t2)

    for t in threads:
        t.join()

def sleep(key='ksikka'):
    machines = Machine.load_files(key='prod') # machine name => machine
    containers = Container.load_files(machines, key=key) # deploy id => container

    for m in machines.values():
        target_containers = [c for c in containers.values() if c.machine == m]
        m.bulk_sleep(target_containers)


def sleepdev():
    sleep(key='ksikka')
    sleep(key='ican')
    sleep(key='abhi')
    sleep(key='nafiul')

if __name__ == "__main__":
    sleepdev()

