#!/usr/bin/env python

from __future__ import print_function
import sys
import telnetlib
import re

'''
This script connects to the grandMA2 via telnet and waits for an error message starting with MpvDo
Add "MpvDo Play file.avi" as CMD in a cue to play the file
and "MpvDo Show file.png" to show an image
and "MpvDo Stop" to blank the screen

The MpvDo command of course does not exist in grandMA which generates an error message which is sent via telnet.
A litte hacky but it works :)
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

conn = telnetlib.Telnet()
conn.open("192.168.178.63", 30000)
try:
    eprint("connected")
    while 1:
        read = conn.read_until("\n")
        #eprint(ashex2(read))
        match = re.search(r"Error : MpvDo (?P<cmd>\w+)( (?P<arg>[a-zA-Z0-9_\.\-]+))?", read)
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
conn.close()
