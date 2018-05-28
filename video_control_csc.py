#!/usr/bin/env python

from __future__ import print_function
import sys
import socket
import re
import argparse
import StringIO

'''
This script opens a server socket on port 4243 and waits for a message starting with MpvDo
"MpvDo Play file.avi" to play the file
"MpvDo Show file.png" to show an image
"MpvDo Stop" to blank the screen
'''

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def ashex(my_hex):
    return " ".join(hex(ord(n)) for n in my_hex)

def ashex2(inputtext):
    replchars = re.compile(r'[\n\r]')
    def replchars_to_hex(match):
        return r'\x{0:02x}'.format(ord(match.group()))
    return replchars.sub(replchars_to_hex, inputtext)

serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 4243))
serversocket.listen(5)
while 1:
    eprint("waiting for connection")
    (clientsocket, address) = serversocket.accept()
    eprint("got connection")
    f = clientsocket.makefile()
    try:
        while 1:
            read = f.readline()
            if read == '':
                break
            eprint(ashex2(read))
            match = re.search(r"MpvDo (?P<cmd>\w+)( (?P<arg>[a-zA-Z0-9_\.\-]+))?", read)
            if match:
                if match.group('cmd') == "Play":
                    sys.stdout.write('loadfile {}\n'.format(match.group('arg')))
                    sys.stdout.flush()
                    sys.stdout.write('seek 0.0 absolute\n')
                    sys.stdout.flush()
                    sys.stdout.write('set pause no\n')
                    sys.stdout.flush()
                elif match.group('cmd') == "Show":
                    sys.stdout.write('loadfile {}\n'.format(match.group('arg')))
                    sys.stdout.flush()
                    sys.stdout.write('set pause yes\n')
                    sys.stdout.flush()
                    sys.stdout.write('seek 0.0 absolute\n')
                    sys.stdout.flush()
                elif match.group('cmd') == "Stop":
                    sys.stdout.write('loadfile black.png\n')
                    sys.stdout.flush()
                    sys.stdout.write('set pause yes\n')
                    sys.stdout.flush()
                    sys.stdout.write('seek 0.0 absolute\n')
                    sys.stdout.flush()
                else:
                    eprint("Unknown command")
    except Exception as ex:
        eprint(ex)
    clientsocket.shutdown(socket.SHUT_RDWR)
    clientsocket.close()
