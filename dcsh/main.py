
from __future__ import absolute_import, print_function

import argparse
import json
import os
import subprocess
import sys
import time

import requests

DISPATCHER = "localhost:5000"


def parse_args():
    """
    Parse arguments provided at the command line

    returns an ordered pair: (script, public_key) where script is a string with
    the contents of the script file to be executed and public_key is a string
    with the contents of the public key file to be used for authentication
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('script', help="Path of the script file to be executed")
    parser.add_argument('--key-file', required=False,
                        help=("Path to the public key file dcsh should use to "
                              "identify itself -- omitting this parameter means "
                              "dcsh will extract the required identity from the "
                              "running ssh agent"))
    args = parser.parse_args()
    # TODO positional arguments should be collected and passed to the dispatcher

    with open(sys.argv[1], 'rb') as f:
        script = f.read()

    if args.key_file:
        public_key = open(args.key_file, 'rb').read()
    else:
        public_key = subprocess.check_output(["ssh-add", "-L"])

    return script, public_key


def main():
    """
    Run a shell script on a datacenter node
    """
    script, public_key = parse_args()
    resp = requests.post(
        url="http://%s/run" % DISPATCHER,
        data=json.dumps([script, public_key]),
        headers={'Content-Type': 'application/octet-stream'})

    _id = resp.text
    info = {}
    running = False
    while not running:
        time.sleep(1)
        resp = requests.get(
            url=("http://%s/job/{0}" % DISPATCHER).format(_id))
        info = resp.json()
        running = info["running"]

    cmd = [
        'ssh',
        "%s@%s" % ("root", info["ip"]),
        "-p",
        str(info["port"]),
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "StrictHostKeyChecking=no",
        "-q",
    ]

    os.execvp("ssh", cmd)
