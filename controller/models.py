from filereader import get_lines_from_files

class Machine(object):
    def __init__(self, name, host):
        self.name = name
        self.host = host

    @classmethod
    def load_state(cls, key='*'):
        lines = get_lines_from_files('machine', key)
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


class Container(object):
    def __init__(self, d_id, machine):
        self.d_id = d_id
        self.machine = machine

    @classmethod
    def load_state(cls, key='*'):
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

            containers[d_id] = Container(d_id, machine_id)

        return containers
