#!/usr/bin/python3
usage = """Usage:
python unix-fd-service.py <file name> &
python unix-fd-client.py
"""


import gobject

import dbus
import dbus.service
import dbus.mainloop.glib
import sys
import random

class SomeObject(dbus.service.Object):

    counter = 0

    @dbus.service.method("com.example.SampleInterface",
                         in_signature='', out_signature='h')
    def GetFd(self):
        self.counter = (self.counter + 1) % 3

        if self.counter == 0:
            print "sending UnixFd(filelike)"
            return dbus.types.UnixFd(f)
        elif self.counter == 1:
            print "sending int"
            return f.fileno()
        else:
            print "sending UnixFd(int)"
            return dbus.types.UnixFd(f.fileno())

if len(sys.argv) < 2:
    print usage
    sys.exit(1)

f = file(sys.argv[1], "r")

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.example.SampleService", session_bus)
    object = SomeObject(session_bus, '/SomeObject')

    mainloop = gobject.MainLoop()
    print("Running fd service.")
    print usage
    mainloop.run()
