#!/usr/bin/python3

import time

usage = """Usage:
python unix-fd-service.py <file name> &
python unix-fd-client.py
"""

import sys
from traceback import print_exc
import os

import dbus

def main():
    bus = dbus.SessionBus()

    try:
        remote_object = bus.get_object("com.example.SampleService",
                                       "/SomeObject")

    except dbus.DBusException:
        print_exc()
        print usage
        sys.exit(1)

    iface = dbus.Interface(remote_object, "com.example.SampleInterface")

    # UnixFd is an opaque object that takes care of received fd
    fd_object = iface.GetFd()
    print fd_object

    # Once we take the fd number, we are in charge of closing it!
    fd = fd_object.take()
    print fd

    # We want to encapsulate the integer fd into a Python file or socket object
    f = os.fdopen(fd, "r")

    # If it were an UNIX socket we would do
    # sk = socket.fromfd(fd, socket.AF_UNIX, socket.SOCK_STREAM)
    # os.close(fd)
    #
    # fromfd() dup()s the descriptor so we need to close the original,
    # otherwise it 'leaks' (stays open until program exits).

    f.seek(0)
    print f.read()

if __name__ == '__main__':
    main()
