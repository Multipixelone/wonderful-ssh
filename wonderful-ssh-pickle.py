#!/usr/bin/python3
import json
import click
from subprocess import call


__author__ = "Multipixelone"


@click.group()
def main():
    """Cross-platform program written in Python3 to manage SSH Hosts."""
    pass

@main.command()
@click.argument('server')
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


@main.command()
def list():
    """List configured hosts."""
    with open('store.json') as store:
        d = json.load(store)
        global hosts
        hosts = d['hosts']
    print(json.dumps(hosts, indent=4, sort_keys=True))


@main.command()
@click.argument('Easy_Name')
def add(easy_name):
    """Add server to json store."""
    pretty_name = input("What is a pretty name for your server ? ")
    address = input("What is your server address ? ")
    login = input("What is your login to your server ? ")
    key = input("If you use a key, what is the path to your key ? ")
    #new = {easy_name: {"name": pretty_name, "address": address, "login": login, "key": key}}
    # new = {"falcon": {"name": "Falcon", "address": "192.168.123.123", "login": "tunnel", "key": ""},
    darray = {}
    darray = 
    darray['name'] = pretty_name
    darray['address'] = address
    darray['login'] = login
    darray['key'] = key
    new = json.dumps(darray)
    print(new)
    with open("store.json", "ab+") as f:
        f.seek(0, 2)
        if f.tell() == 0:
            f.write(json.dumps([new]).encode())
        else:
            f.seek(-4, 2)
            f.truncate()
            f.write(','.encode())
            f.seek(-1, 2)
            f.write(json.dumps(new, indent=4, sort_keys=True).encode())
            f.write('}'.encode())

if __name__ == "__main__":
    main()
