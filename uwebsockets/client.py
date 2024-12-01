"""
Websockets client for MicroPython without ussl (for wss://)
WARNING: This implementation is not secure for public networks.

Modified from: https://github.com/danni/uwebsockets/tree/esp8266
"""

import usocket as socket
import ubinascii as binascii
import urandom as random

from .protocol import Websocket, urlparse


class WebsocketClient(Websocket):
    is_client = True


def connect(uri):
    """
    Connect to a websocket (supports ws:// and wss:// without SSL).
    """

    uri = urlparse(uri)
    assert uri

    sock = socket.socket()
    addr = socket.getaddrinfo(uri.hostname, uri.port)
    sock.connect(addr[0][4])

    if uri.protocol == 'wss':
        print(
            "WARNING: Using 'wss://' without SSL. This is insecure and should only be used in trusted networks."
        )

    def send_header(header, *args):
        sock.write(header % args + '\r\n')

    key = binascii.b2a_base64(bytes(random.getrandbits(8)
                                    for _ in range(16)))[:-1]

    send_header(b'GET %s HTTP/1.1', uri.path or '/')
    send_header(b'Host: %s:%s', uri.hostname, uri.port)
    send_header(b'Connection: Upgrade')
    send_header(b'Upgrade: websocket')
    send_header(b'Sec-WebSocket-Key: %s', key)
    send_header(b'Sec-WebSocket-Version: 13')
    send_header(b'Origin: http://{hostname}:{port}'.format(
        hostname=uri.hostname,
        port=uri.port)
    )
    send_header(b'')

    header = sock.readline()[:-2]
    assert header.startswith(b'HTTP/1.1 101 '), header

    while header:
        header = sock.readline()[:-2]

    return WebsocketClient(sock)
