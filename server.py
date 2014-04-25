#!/usr/bin/env python

from flask import Flask, request
app = Flask(__name__)

import re
import json
from controller.models import Machine, Container

@app.route('/')
def home():
    return 'Yolo'

@app.route('/deployment/list', methods=['GET'])
def get_deployments():
    username = request.args.get('username', '')
    if username == '':
        return 'plz pass username as a query string arg.', 400

    username = username.lower()

    if not re.match(r'^[0-9a-z]+$', username):
        return 'invalid username, it must be alphanumeric only for now.', 400

    ms = Machine.load_files(key='prod')
    containers = Container.load_files(ms, key=username)

    return json.dumps(containers.keys())





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)

