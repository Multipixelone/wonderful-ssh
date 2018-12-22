#!/usr/bin/python3
import json
from subprocess import call


def main():
    """Cross-platform program written in Python3 to manage SSH Hosts."""
    connect("OpenSUSE")


__author__ = "Multipixelone"


def connect(server):
    """Connect to host via SSH."""
    with open('store.json') as store:
        d = json.load(store)
        global hosts
        hosts = d['hosts']
    global host
    global name
    global address
    global login
    global key
    host = hosts[server]
    name = host['name']
    address = host['address']
    login = host['login']
    key = host['key']
    print("Connecting to " + name + " at " + address + " using username " + login)
    if host['key']:
        call(["ssh", "-i" + key, login + "@" + address])
    else:
        call(["ssh", login + "@" + address])


if __name__ == "__main__":
    # execute only if run as a script
    main()
