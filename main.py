# Copyright (c) 2018 Amit Chahar
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from bluetooth import *
import sys
import bcs_pty

addr = None

# search for the Bluetooth-Server-Shell service
print("Searching all nearby Bluetooth devices for Bluetooth-Server-Shell...")
uuid = "347fb489-38fb-4325-898b-ec28b40c3c46"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print("couldn't find the Bluetooth-Server-Shell service. Please try again.")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

print("connected.  type stuff")
while True:
    # data = raw_input()
    # if len(data) == 0: break
    # sock.send(data)
    bcs_pty.spawn("/bin/bash", sock)

sock.close()
