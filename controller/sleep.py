#!/usr/bin/env python


from models import Machine, Container

def sleep(key='alpha-dev'):
    machines = Machine.load_files(key=key) # machine name => machine
    print machines
    containers = Container.load_files(machines, key='*') # deploy id => container

    for m in machines.values():
        target_containers = [c for c in containers.values() if c.machine == m and c.d_id not in ['zenrez','adshare']]
        m.bulk_sleep(target_containers)


if __name__ == "__main__":
    # sleep all free machines
    sleep('alpha-free')
    # sleep all dev machines
    sleep('alpha-dev')

