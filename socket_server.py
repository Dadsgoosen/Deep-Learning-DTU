from socket import socket, AF_INET, SOCK_STREAM
import selectors
import types
from abc import ABC, abstractmethod
from threading import Thread
from typing import Tuple, Union
import json


class SocketServer(ABC, Thread):

    def __init__(self, host: str, port: int):
        self.sel: selectors.DefaultSelector = selectors.DefaultSelector()
        # Start up the socket
        self.lsock = socket(AF_INET, SOCK_STREAM)
        self.lsock.bind((host, port))
        self.lsock.listen()
        # Ready to listen
        print('listening on', (host, port))
        # Set the socket to not block so that we can accept multiple connections
        self.lsock.setblocking(False)
        # Register the socket
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)
        ABC.__init__(self)
        Thread.__init__(self)

    def run(self) -> None:
        while True:
            self.on_step()
            events = self.sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.__accept_wrapper(key.fileobj)
                else:
                    self.__service_connection(key, mask)
            self.on_step()


    def on_step(self):
        pass

    def on_connection_closed(self, addr: Tuple[str, int]):
        pass

    def on_accept_connection(self, sock: socket, addr: Tuple[str, int], data: types.SimpleNamespace):
        pass

    def on_message_received(self, sock: socket, data, received_data: str, addr: Tuple[str, int]) -> None:
        pass

    def send_message(self, data, send: Union[str, dict, list]):
        if isinstance(send, (dict, list)):
            outbound = json.dumps(send)
        else:
            outbound = send
        data.outb += outbound.encode()

    def __close_connection(self, sock: socket, data):
        print('Closing connection to {}'.format(data.addr))
        self.on_connection_closed(data.addr)
        self.sel.unregister(sock)
        sock.close()

    def __accept_wrapper(self, sock: socket):
        conn, addr = sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        self.on_accept_connection(sock, addr, data)

    def __service_connection(self, key, mask):
        sock: socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(6144)
            if recv_data:
                self.on_message_received(sock, data, recv_data.decode(), data.addr)
            else:
                self.__close_connection(sock, data)
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print('Sending {} to {}'.format(repr(data.outb), data.addr))
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]

