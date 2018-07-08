
import os
from typing import Callable
from threading import Thread
from smallMITM.fake_client import FakeClient
from smallMITM.fake_server import FakeServer
import smallMITM.network_type as network_type

def deault_parse_function(data: bytes,intro: str) -> bytes:
    """Default parse function. Print the data and who sent them and return it unchanged."""
    print("[Received from {intro}]: {data}\n\n".format(intro=intro,data=str(data)))
    return data

class MITM(Thread):
    """Man-In-The-Middle Class. It Listen on the port server_port and forward the data
    to the host on port client_port. data before being forwarded pass throught the
    parse_function which is by default set to a function that only print the data
    and return it unchanged."""

    def __init__(self):
        """Costructor of the MITM Class. It's supposed to be initialized
        and then all the settings setted by setters methodself."""
        super(MITM, self).__init__()
        self.buffer_size      =  10485760 #10MB
        self.host             = '0.0.0.0' # all ip
        self.client_port      = 80
        self.server_port      = 80
        self.parse_function   = deault_parse_function
        self.network_type     = network_type.TCP

    def __repr__(self):
        """The Official Rappresentation of the MITM class: It print the value of all the settings of the class."""
        dict = self.__dict__
        output = ""
        output += "MITM(0.0.0.0:{server_port} -> {host}:{client_port}):\n".format(**dict)
        output += "\tbuffer_size: {buffer_size}\n".format(**dict)
        output += "\thost: {host}\n".format(**dict)
        output += "\tclient_port: {client_port}\n".format(**dict)
        output += "\tserver_port: {server_port}\n".format(**dict)
        output += "\tnetwork_type: {network_type}\n".format(**dict)
        output += "\tdata parsing function: {parse_function}\n".format(**dict)
        return output

    def set_parse_function(self,function: Callable[[bytes,str],bytes]):
        """Setter method for the parse_function attribute."""
        self.parse_function = function
        return self

    def set_host(self,host: str):
        """Setter method for the host attribute."""
        self.host = host
        return self

    def set_server_port(self,server_port: int):
        """Setter method for the server_port attribute."""
        self.server_port = server_port
        return self

    def set_client_port(self,client_port: int):
        """Setter method for the client_port attribute."""
        self.client_port = client_port
        return self

    def set_buffer_size(self,buffer_size: int):
        """Setter method for the buffer_size attribute."""
        self.buffer_size = buffer_size
        return self

    def set_network_type(self,network_type):
        """Setter method of the network_type attribute. It can be either TCP or UDP"""
        self.network_type = network_type
        return self

    def run(self) -> None:
        """Create the FakeClient and FakeServer and start them."""
        print("[proxy(0.0.0.0:{server_port} -> {host}:{client_port})] setting up".format(server_port=self.server_port,client_port=self.client_port,host=self.host))
        # create the two proxy
        fake_client = FakeClient().set_buffer_size(self.buffer_size).set_parse_function(self.parse_function)
        fake_server = FakeServer().set_buffer_size(self.buffer_size).set_parse_function(self.parse_function)

        # setup the port and host
        fake_client.set_port(self.client_port).set_network_type(self.network_type).set_host(self.host)
        fake_server.set_port(self.server_port).set_network_type(self.network_type)

        # cross link
        fake_client.set_fake_server(fake_server).create()
        fake_server.set_fake_client(fake_client).create()

        print("[proxy(0.0.0.0:{server_port} -> {host}:{client_port})] connection established".format(server_port=self.server_port,client_port=self.client_port,host=self.host))

        fake_server.start()
        fake_client.start()
