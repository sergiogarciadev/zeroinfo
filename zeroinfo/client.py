# -*- coding: utf-8 -*-
"""Client classes."""

import socket
import struct

from asyncio import DatagramProtocol

BROADCAST_PORT = 9999
BROADCAST_ADDR = "239.255.255.250"


class ClientProtocol(DatagramProtocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        sock = transport.get_extra_info('socket')
        sock.settimeout(3)
        ttl = struct.pack('@i', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        print(f'Send: {len(self.message)}')
        self.transport.sendto(self.message.encode(), (BROADCAST_ADDR, BROADCAST_PORT))

    def datagram_received(self, data, addr):
        print("Received:", data.decode())
        self.loop.stop()

        print("Close the socket")
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        self.loop.stop()


class Client(object):
    """Client class"""

    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self.protocol = None

    def start(self):
        """Start the client."""

        message = "Hello World!" * 5000
        addrinfo = socket.getaddrinfo(BROADCAST_ADDR, None)[0]
        sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        connect = self.loop.create_datagram_endpoint(
            lambda: ClientProtocol(message, self.loop),
            sock=sock,
        )
        self.transport, self.protocol = self.loop.run_until_complete(connect)


    def stop(self):
        """Stop the client."""

        self.transport.close()
