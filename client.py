#!/usr/bin/python3

usage = """Usage:
python custom_service.py &
python client.py
python client.py --exit-service
"""


import sys
from traceback import print_exc

import dbus

def main():
    bus = dbus.SessionBus()

    try:
        remote_object = bus.get_object("com.example.SampleService",
                                       "/SomeObject")

        # you can either specify the dbus_interface in each call...
        hello_reply_list = remote_object.HelloWorld("Hello from client.py!",
            dbus_interface = "com.example.SampleInterface")
    except dbus.DBusException:
        print_exc()
        print usage
        sys.exit(1)

    print (hello_reply_list)

    # ... or create an Interface wrapper for the remote object
    iface = dbus.Interface(remote_object, "com.example.SampleInterface")

    hello_reply_tuple = iface.GetTuple()

    print hello_reply_tuple

    hello_reply_dict = iface.GetDict()

    print hello_reply_dict

    # D-Bus exceptions are mapped to Python exceptions
    try:
        iface.RaiseException()
    except dbus.DBusException as e:
        print str(e)

    # introspection is automatically supported
    print remote_object.Introspect(dbus_interface="org.freedesktop.DBus.Introspectable")

    if sys.argv[1:] == ['--exit-service']:
        iface.Exit()

if __name__ == '__main__':
    main()
