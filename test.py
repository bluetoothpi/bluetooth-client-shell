import os
import pty
import subprocess
import select
import sys


def get_cli_subprocess_handle():
    masterPTY, slaveTTY = pty.openpty()
    subprocess.Popen('/bin/bash', shell=True, stdin=slaveTTY, stdout=slaveTTY, stderr=slaveTTY)

    while True:
        readers, _, _ = select.select([sys.stdin, masterPTY], [], [])
        for reader in readers:
            if reader is sys.stdin:
                print("reading user_input")
                write_all(masterPTY, sys.stdin.readline())
            else:
                print "reading from masterpty"
                data = os.read(masterPTY, 1024)
                print(data)


def write_all(masterPTY, data):
    """Successively write all of data into a file-descriptor."""
    while data:
        chars_written = os.write(masterPTY, data)
        data = data[chars_written:]
    return data


pty.spawn("/bin/bash")
get_cli_subprocess_handle()