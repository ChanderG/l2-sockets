#!/usr/bin/env python3

""" l2.py - Simple L2 packet injector and sniffer
Usage:
  l2.py inject <interface>
  l2.py sniff
"""
from docopt import docopt

import socket
import struct

def inject(intf):
    # We are using a randomly chosen, hopefully unassigned EtherType of 0x6001
    # See: https://www.wikipedia.org/wiki/EtherType
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x6001))
    s.bind((intf, socket.htons(0x6001)))
    # dummy destination and source macs, since we are not going to be using it anyway
    packet = struct.pack("!6s6s2s", b'\xaa\xaa\xaa\xaa\xaa\xaa', b'\xbb\xbb\xbb\xbb\xbb\xbb', b'\x60\x01')

    s.send(packet + b"Hello L2!")

def sniff():
    # Note: we start receiving from pretty much all interfaces
    # But, since we have specified an un-used EtherType, we don't end up capturing
    # a flood of other (actual) traffic
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x6001))

    while True:
        pkt = s.recvfrom(30)
        (data, addrinfo) = pkt
        ethHeader = struct.unpack("!6s6s2s", data[0:14])
        print("Packet: Intf={0}, Header={1}, Message={2}".format(addrinfo[0], ethHeader, data[14:]))

def main():
    args = docopt(__doc__)

    if args["inject"]:
        inject(args["<interface>"])
    elif args["sniff"]:
        sniff()
    else:
        RuntimeError("No command specified.")

if __name__ == "__main__":
    main()
