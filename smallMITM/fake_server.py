
import socket
from typing import Callable
from threading import Thread
import smallMITM.network_type as network_type

class FakeServer(Thread):

    def __init__(self):
        super(FakeServer, self).__init__()
        self.fake_client      = None
        self.buffer_size      = 4096
        self.port             = 80
        self.parse_function   = None
        self.network_type     = network_type.TCP

    def set_buffer_size(self,buffer_size: int):
        self.buffer_size = buffer_size
        return self

    def set_parse_function(self,function: Callable[[bytes,str],bytes]):
        self.parse_function = function
        return self

    def set_network_type(self,network_type):
        self.network_type = network_type
        return self

    def set_port(self,port: int):
        self.port = port
        return self

    def set_fake_client(self,fake_client):
        self.fake_client = fake_client
        return self

    def create(self):
        self.address = "0.0.0.0:{port}".format(port=self.port)
        self.listen_socket = self.network_type().get_socket()
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(("0.0.0.0", self.port))
        self.listen_socket.listen(1)
        self.accept_socket, addr = self.listen_socket.accept()

    def send(self,data) -> None:
        self.accept_socket.send(data)

    def run(self) -> None:
        try:
            while True:
                data = self.accept_socket.recv(self.buffer_size)
                if data:
                    data = self.parse_function(data,self.address)
                    if(self.fake_client):
                        self.fake_client.send(data)

        except KeyboardInterrupt:
            print("Closing the FakeClient")
        finally:
            self.accept_socket.close()
            self.listen_socket.close()
