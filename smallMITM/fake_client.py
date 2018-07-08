
import socket
from typing import Callable
from threading import Thread
import smallMITM.network_type as network_type


class FakeClient(Thread):
    def __init__(self):
        super(FakeClient, self).__init__()
        self.fake_server      = None
        self.buffer_size      = 4096
        self.host             = '0.0.0.0' # all ip
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

    def set_host(self,host: str):
        self.host = host
        return self

    def set_port(self,port: int):
        self.port = port
        return self

    def set_fake_server(self,fake_server):
        self.fake_server = fake_server
        return self

    def create(self):
        self.address = "[received from {host}:{port}]".format(host=self.host,port=self.port)
        self.send_socket = self.network_type().get_socket()
        self.send_socket.connect((self.host, self.port))

    def send(self,data) -> None:
        self.send_socket.send(data)

    def run(self) -> None:
        try:
            while True:
                data = self.send_socket.recv(self.buffer_size)
                if data:
                    data = self.parse_function(data,self.address)
                    if(self.fake_server != None):
                        self.fake_server.send(data)
        except KeyboardInterrupt:
            print("Closing the FakeClient")
        finally:
            self.send_socket.close()
