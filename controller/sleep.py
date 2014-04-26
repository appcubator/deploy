#!/usr/bin/env python


from models import Machine, Container

def sleep(key='ksikka'):
    machines = Machine.load_files(key='prod') # machine name => machine
    containers = Container.load_files(machines, key=key) # deploy id => container

    for m in machines.values():
        target_containers = [c for c in containers.values() if c.machine == m and c.d_id not in ['zenrez','adshare']]
        m.bulk_sleep(target_containers)


def sleepdev():
    sleep(key='ksikka')
    sleep(key='ican')
    sleep(key='abhi')
    sleep(key='nafiul')

if __name__ == "__main__":
    sleep('prod')
    #sleepdev()

