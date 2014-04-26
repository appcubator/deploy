import os
import glob

j = os.path.join # too damn long

STATE_DIR = j(os.path.dirname(__file__), '..', '..', 'cluster-conf')

def get_lines_from_files(prefix, key):
    lines = []
    for filepath in glob.glob(j(STATE_DIR, '{prefix}-{key}.txt'.format(prefix=prefix, key=key))):
        with open(filepath) as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith('#'):
                    continue

                lines.append(line)
    return lines

if __name__ == "__main__":
    # stupid test

    lines = get_lines_from_files('deploy', 'prod-*')

    print lines
