#!/usr/bin/env python3

""" l2.py - Simple L2 packet injector and sniffer
Usage:
  l2.py inject <interface> [--src-mac=<addr>] [--dest-mac=<addr>]
  l2.py sniff
"""
from docopt import docopt

import socket
import struct
import binascii
import logging

def _mac_hex_builder(addr):
    if addr == None:
        logging.info("No MAC addr provided, using dummy values!")
        return b'\xaa\xaa\xaa\xaa\xaa\xaa'

    addstr = "".join(addr.split(":"))
    hexstr = binascii.unhexlify(addstr)
    logging.info("Addr string: %s, hex str: %s", addr, hexstr)
    return hexstr

def inject(intf, src, dest):
    # We are using a randomly chosen, hopefully unassigned EtherType of 0x6001
    # See: https://www.wikipedia.org/wiki/EtherType
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x6001))
    s.bind((intf, socket.htons(0x6001)))
    # dummy destination and source macs, since we are not going to be using it anyway
    packet = struct.pack("!6s6s2s", _mac_hex_builder(dest), _mac_hex_builder(src), b'\x60\x01')

    ret = s.send(packet + b"Hello L2!")
    logging.info("Sent packet: %d bytes.", ret)

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
    logging.basicConfig(level=logging.INFO)
    args = docopt(__doc__)

    if args["inject"]:
        inject(args["<interface>"], args["--src-mac"], args["--dest-mac"])
    elif args["sniff"]:
        sniff()
    else:
        RuntimeError("No command specified.")

if __name__ == "__main__":
    main()
