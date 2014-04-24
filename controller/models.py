from filereader import get_lines_from_files


class Machine(object):
    def __init__(self, name, host):
        self.name = name
        self.host = host

    @classmethod
    def load_state(cls, key='*'):
        lines = get_lines_from_files('machines', key)
        machines = {}
        for line in lines:
            tokens = line.split()
            if len(tokens) != 2:
                raise Exception('Expected 2 tokens per line, found %d' % len(tokens))

            machine_id = tokens[0]
            host_addr = tokens[1]

            if machine_id in machines:
                raise Exception('Duplicate machine id found: %s' % machine_id)

            machines[machine_id] = Machine(machine_id, host_addr)
        return machines

    @classmethod
    def bulk_create(cls, containers):
        pass

    @classmethod
    def bulk_delete(cls, containers):
        pass


class Container(object):
    def __init__(self, d_id, machine):
        self.d_id = d_id
        self.machine = machine

    @classmethod
    def load_state(cls, machines, key='*'):
        lines = get_lines_from_files('deploy', key)
        containers = {}
        for line in lines:
            tokens = line.split()

            if len(tokens) != 2:
                raise Exception('Expected 2 tokens per line, found %d' % len(tokens))

            d_id = tokens[0]
            machine_id = tokens[1]

            if d_id in containers:
                raise Exception('Duplicate deploy id found: %s' % d_id)

            if machine_id not in machines:
                raise Exception('Machine with this id not found: %s' % machine_id)

            machine = machines[machine_id]

            containers[d_id] = Container(d_id, machine)

        return containers

if __name__ == "__main__":
    # stupid test

    machines = Machine.load_state() # machine name => machine
    print machines
    containers = Container.load_state(machines) # deploy id => container
    print containers
