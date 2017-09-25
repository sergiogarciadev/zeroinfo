# -*- coding: utf-8 -*-
"""Server classes."""

import logging
import socket
import struct

from asyncio import DatagramProtocol


BROADCAST_PORT = 9999
BROADCAST_ADDR = "239.255.255.250"


class ServerProtocol(DatagramProtocol):
    """Zeroinfo server protocol"""

    def __init__(self):
        self.transport = None
        self.sock = None
        self.logger = logging.getLogger('zeroinfo.server')

    def connection_made(self, transport):
        self.transport = transport
        self.sock = transport.get_extra_info("socket")
        self.sock.settimeout(3)
        ttl = struct.pack('@i', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    def connection_lost(self, exc):
        print('connection_lost')

    def datagram_received(self, data, addr):
        message = data.decode()
        print(f'Received {len(message)} from {addr}')
        self.transport.sendto('ack'.encode(), addr)

    def error_received(self, exc):
        print('error_received')


class Server(object):
    """Server class"""

    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self.protocol = None

    def start(self):
        """Start the server."""

        addrinfo = socket.getaddrinfo(BROADCAST_ADDR, None)[0]
        sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
        sock.bind(('', BROADCAST_PORT))
        mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # One protocol instance will be created to serve all client requests
        listen = self.loop.create_datagram_endpoint(
            ServerProtocol,
            sock=sock,
        )
        self.transport, self.protocol = self.loop.run_until_complete(listen)

    def stop(self):
        """Stop the server."""

        self.transport.close()
