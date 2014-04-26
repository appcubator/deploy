"""
In a deploy cluster,
    you have machines, namespaced for muliple layers of performance and isolation
    you have containers, namespaced for different user/agents (paid vs not paid vs api etc.)
"""

from filereader import get_lines_from_files
import subprocess
import json
from threading import Thread

import os
j = os.path.join

SCRIPT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

class Machine(object):
    """
    Represents a Machine hosting apps.

    The Machine must have a user called deployer,
        with a specific public key,
        which can be setup using the cloudinit.yml in the repo.

    This machine must have the private key
        saved as pk.pem in the root of the repo,
        not committed since it's a secret.
    """

    def __init__(self, name, host):
        self.name = name
        self.host = host

    def __repr__(self):
        return "%s:%s" % (self.name, self.host)

    def __eq__(self, other):
        return self.host == other.host

    @classmethod
    def load_files(cls, key='*'):
        """
        Read from machines-<key>-*.txt files,
            do some additional validation.
        Outputs a map from machine name to machine object.
        """
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


    def load_existing_containers(self):
        """
        Calls the remote docker_dump scripts,
        Outputs a map from container_id to containr object
        """
        p = subprocess.Popen([j(SCRIPT_ROOT, 'remote', 'docker_dump.sh'), self.host],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

        out, err = p.communicate()

        # check empty case
        if 'Usage' in err:
            print "Warning: Saw usage string. Usually this indicates no containers, but I can't be sure."
            print "Err:" + err
            return {}

        containers = {}

        configs = json.loads(out)

        for config in configs:
            name = config['Name']
            # ie, /devmon-zenrez
            if name.startswith('/devmon-'):
                d_id = name.replace('/devmon-', '')
                c = Container(d_id, self)

                if d_id in containers:
                    raise Exception('Duplicate deploy id found: %s' % d_id)

                containers[d_id] = c
            else:
                print 'Skipping container, not a deploy concern: ' + name

        return containers


    def bulk_create(self, containers):
        """
        Create the given containers on this machine.
            Assumes that containers is a collection of Container objects.
        """
        if len(containers) == 0:
            return

        nl_sep_deploy_ids = '\n'.join([c.d_id for c in containers])

        p = subprocess.Popen([j(SCRIPT_ROOT, 'remote', 'bulk_create.sh'), self.host],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)

        out, err = p.communicate(nl_sep_deploy_ids)

        p.wait()

    def bulk_sleep(self, containers):
        """
        Sleep the given containers on this machine.
            Assumes that containers is a collection of Container objects.
        """
        if len(containers) == 0:
            return

        nl_sep_deploy_ids = '\n'.join([c.d_id for c in containers])

        p = subprocess.Popen([j(SCRIPT_ROOT, 'remote', 'bulk_sleep.sh'), self.host],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)

        out, err = p.communicate(nl_sep_deploy_ids)

        p.wait()

    def bulk_destroy(self, containers):
        """
        Destroy the given containers on this machine.
            Assumes that containers is a collection of Container objects.
        """
        if len(containers) == 0:
            return

        nl_sep_deploy_ids = '\n'.join([c.d_id for c in containers])

        p = subprocess.Popen([j(SCRIPT_ROOT, 'remote', 'bulk_destroy.sh'), self.host],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)

        out, err = p.communicate(nl_sep_deploy_ids)

        p.wait()

    def converge(self, target_containers):
        """
        Input the list of Containers you wish to be running on this machine.
          Note: you must start the threads t1 and t2 yourself.
          This allows you to create all the containers before destroying them on their original hosts for migrations without downtime.
        """
        remote_containers = self.load_existing_containers()

        print 'Remote Containers', remote_containers

        to_create = [ c for c in target_containers if c.machine == self and c.d_id not in remote_containers ]
        print "Task created to create: ", to_create
        t1 = Thread(target=self.bulk_create, args=(to_create,))

        to_delete = [ c for d_id, c in remote_containers.iteritems() if c.machine == self and c not in target_containers ]
        print "Task created to destroy: ", to_delete
        t2 = Thread(target=self.bulk_destroy, args=(to_delete,))

        return (to_create, to_delete, t1, t2)


class Container(object):
    """
    Represents a Container, has a reference to its Machine.
    """

    def __init__(self, d_id, machine):
        self.d_id = d_id
        self.machine = machine

    def __repr__(self):
        return "%s@%s" % (self.d_id, self.machine.name)

    def __eq__(self, other):
        return self.d_id == other.d_id

    @classmethod
    def load_files(cls, machines, key='*'):
        """
        Read from deploy-<key>-*.txt files,
            do some additional validation.

        Pass in the result of Machine.load_files() so I can link
            containers to machines.
        """
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
                print "Warning: Skipping container since it's machine was not selected: (%s, %s)" % (d_id, machine_id)
                continue

            machine = machines[machine_id]

            containers[d_id] = Container(d_id, machine)

        return containers

