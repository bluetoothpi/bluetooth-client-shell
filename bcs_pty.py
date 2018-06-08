# Copyright (c) 2018 Amit Chahar
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from select import select
import os
import tty

STDIN_FILENO = 0
STDOUT_FILENO = 1
STDERR_FILENO = 2


def send_to_server(fd, data):
    """Write all the data to a descriptor."""
    while data != '':
        n = fd.send(data)
        data = data[n:]


def read_from_stdin(fd):
    """Default read function."""
    return os.read(fd, 1024)


def recv_from_server(fd):
    """Default read function."""
    return fd.recv(1024)


def copy_and_send(master_fd):
    """Parent copy loop.
    Copies
            pty master -> standard output   (master_read)
            standard input -> pty master    (stdin_read)"""
    fds = [master_fd, STDIN_FILENO]
    while True:
        rfds, wfds, xfds = select(fds, [], [])
        if master_fd in rfds:
            data = recv_from_server(master_fd)
            if not data:  # Reached EOF.
                fds.remove(master_fd)
            else:
                os.write(STDOUT_FILENO, data)
        if STDIN_FILENO in rfds:
            data = read_from_stdin(STDIN_FILENO)
            if not data:
                fds.remove(STDIN_FILENO)
            else:
                send_to_server(master_fd, data)


def start_client_terminal(sock):
    try:
        mode = tty.tcgetattr(STDIN_FILENO)
        tty.setraw(STDIN_FILENO)
        restore = 1
    except tty.error:    # This is the same as termios.error
        restore = 0
    try:
        copy_and_send(sock)
    except (IOError, OSError):
        if restore:
            tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)
