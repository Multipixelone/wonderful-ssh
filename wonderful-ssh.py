#!/usr/bin/python3
import sqlite3
import click
import subprocess
import datetime
import os
from os.path import expanduser


__author__ = "Multipixelone"
folder = expanduser("~/.config/wonderful-ssh")
config = expanduser("~/.config/wonderful-ssh/store.db")


@click.group()
def main():
    """Cross-platform program written in Python3 to manage SSH Hosts."""
    if not os.path.isdir(folder):
            os.makedirs(folder)
            print("Config directory %s was created." % folder)
    pass


@main.command()
@click.argument('server')
def connect(server):
    """Connect to host via SSH."""
    if os.name == "nt":
        conn = sqlite3.connect('store.db')
    else:
        conn = sqlite3.connect(config)
    c = conn.cursor()
    c.execute("SELECT * FROM servers WHERE host LIKE '%s'" % server)
    host = c.fetchone()
    name = host[1]
    address = host[2]
    login = host[3]
    key = host[4]
    print("Connecting to " + name + " at " + address + " using username " + login)
    type = "CONNECT"
    time = datetime.datetime.now().strftime("%Y-%m-%d %l:%M:%S")
    state = "good"
    print(time)
    c.execute('''CREATE TABLE IF NOT EXISTS log
            (time text, type text, value text, state text)''')
    conn.commit()
    if host[4]:
        try:
            subprocess.run(["ssh", "-i" + key, login + "@" + address], check=True)
            pass
        except EOFError:
            state = "ERRORED"
            pass
        c.execute("INSERT INTO log VALUES (?, ?, ?, ?)", (time, type, address, state))
        conn.commit()
        conn.close()
    else:
        try:
            subprocess.call(["ssh", login + "@" + address])
            pass
        except EOFError:
            state = "ERRORED"
            pass
        c.execute("INSERT INTO log VALUES (?, ?, ?, ?)", (time, type, address, state))
        conn.commit()
        conn.close()


@main.command()
@click.argument('server')
def remove(server):
    """Connect to host via SSH."""
    if os.name == "nt":
        conn = sqlite3.connect('store.db')
    else:
        conn = sqlite3.connect(config)
    c = conn.cursor()
    #c.execute("DELETE FROM servers WHERE host = \"'%s'\"" % server)
    c.execute("DELETE FROM servers WHERE host = \"(?)\"",
        (server))
    conn.commit()
    conn.close()


@main.command()
@click.argument('Easy_Name')
def add(easy_name):
    """Add server to json store."""
    if os.name == "nt":
        conn = sqlite3.connect('store.db')
    else:
        conn = sqlite3.connect(config)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS servers
                (host text, name text, address text, login text, key text)''')
    pretty_name = input("What is a pretty name for your server ? ")
    address = input("What is your server address ? ")
    login = input("What is your login to your server ? ")
    key = input("If you use a key, what is the path to your key ? ")
    c.execute("INSERT INTO servers VALUES (?, ?, ?, ?, ?)", (easy_name, pretty_name, address, login, key))
    conn.commit()
    conn.close()


@main.command()
def list():
    """List configured hosts."""
    if os.name == "nt":
        conn = sqlite3.connect('store.db')
    else:
        conn = sqlite3.connect(config)
    c = conn.cursor()
    c.execute("SELECT * FROM servers")
    print(c.fetchall())
    conn.close()


@main.command()
@click.argument('Server')
def show(server):
    """Show defined servers."""
    if os.name == "nt":
        conn = sqlite3.connect('store.db')
    else:
        conn = sqlite3.connect(config)
    c = conn.cursor()
    c.execute("SELECT * FROM servers WHERE host LIKE '%s'" % server)
    #c.execute('SELECT * FROM servers WHERE host=?', server)
    print(c.fetchone())
    conn.close()


@main.command()
@click.argument('Name')
def search(server):
    """Show defined servers."""
    if os.name == "nt":
        conn = sqlite3.connect('store.db')
    else:
        conn = sqlite3.connect(config)
    c = conn.cursor()
    c.execute('SELECT * FROM servers WHERE host LIKE %?%', server)
    #c.execute('SELECT * FROM servers WHERE host=?', server)
    print(c.fetchone())
    conn.close()


@main.command()
def log():
    """List configured hosts."""
    if os.name == "nt":
        conn = sqlite3.connect('store.db')
    else:
        conn = sqlite3.connect(config)
    c = conn.cursor()
    c.execute("SELECT * FROM log")
    print(c.fetchall())
    conn.close()


if __name__ == "__main__":
    main()
