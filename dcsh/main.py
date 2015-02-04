
from __future__ import absolute_import, print_function

import os
import sys
import time

import requests

def main():
    script = open(sys.argv[1], 'rb').read()

    resp = requests.post(
        url="http://localhost:5000/run",
        data=script,
        headers={'Content-Type': 'application/octet-stream'})

    _id = resp.text
    info = {}
    running = False
    while not running:
        time.sleep(1)
        resp = requests.get(
            url="http://localhost:5000/job/{0}".format(_id))
        info = resp.json()
        running = info["running"]

    cmd = [
        'nc',
        info["ip"],
        str(info["port"])
    ]

    os.execvp("nc", cmd)
