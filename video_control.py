#!/usr/bin/env python

from __future__ import print_function
import socket
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 4243))
serversocket.listen(5)
while 1:
    eprint("waiting for connection")
    (clientsocket, address) = serversocket.accept()
    eprint("got connection")
    while 1:
        try:
            read = clientsocket.recv(1024)
        except Exception as e:
            eprint("Could not read from socket")
            eprint(e)
            break
        if read == '':
            eprint("lost connection")
            break
        eprint("read: " + read)
        if 'PLAY' in read:
            sys.stdout.write('loadfile ffmpeg/alans_dream_aud.mkv\n')
            sys.stdout.flush()
            sys.stdout.write('seek 0.0 absolute\n')
            sys.stdout.flush()
            sys.stdout.write('set pause no\n')
            sys.stdout.flush()
        if 'INTERMISSION' in read:
            sys.stdout.write('loadfile intermission.png\n')
            sys.stdout.flush()
            sys.stdout.write('seek 0.0 absolute\n')
            sys.stdout.flush()
            sys.stdout.write('set pause no\n')
            sys.stdout.flush()
        elif 'STOP' in read:
            sys.stdout.write('loadfile black.png\n')
            sys.stdout.flush()
            sys.stdout.write('set pause yes\n')
            sys.stdout.flush()
            sys.stdout.write('seek 0.0 absolute\n')
            sys.stdout.flush()
        else:
            eprint("Unknown command")
