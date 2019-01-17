#!/usr/bin/python3
import sqlite3
import click
import subprocess


__author__ = "Multipixelone"


@click.group()
def main():
    """Cross-platform program written in Python3 to manage SSH Hosts."""
    pass


@main.command()
@click.argument('server')
def connect(server):
    """Connect to host via SSH."""
    conn = sqlite3.connect('store.db')
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
            break
        except EOFError:
            state = "ERRORED"
            break
        c.execute("INSERT INTO log VALUES (?, ?, ?, ?)", (time, type, address, state))
        conn.commit()
        conn.close()
    else:
        try:
            subprocess.call(["ssh", login + "@" + address])
            break
        except EOFError:
            state = "ERRORED"
            break
        c.execute("INSERT INTO log VALUES (?, ?, ?, ?)", (time, type, address, state))
        conn.commit()
        conn.close()


@main.command()
@click.argument('server')
def remove(server):
    """Connect to host via SSH."""
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    conn.commit()
    conn.close()


@main.command()
@click.argument('Easy_Name')
def add(easy_name):
    """Add server to json store."""
    conn = sqlite3.connect('store.db')
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
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute("SELECT * FROM servers")
    print(c.fetchall())
    conn.close()


@main.command()
@click.argument('Server')
def show(server):
    """Show defined servers."""
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute("SELECT * FROM servers WHERE host LIKE '%s'" % server)
    #c.execute('SELECT * FROM servers WHERE host=?', server)
    print(c.fetchone())
    conn.close()


@main.command()
@click.argument('Name')
def search(server):
    """Show defined servers."""
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute('SELECT * FROM servers WHERE host LIKE %?%', server)
    #c.execute('SELECT * FROM servers WHERE host=?', server)
    print(c.fetchone())
    conn.close()


@main.command()
def log():
    """List configured hosts."""
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute("SELECT * FROM log")
    print(c.fetchall())
    conn.close()


if __name__ == "__main__":
    main()
