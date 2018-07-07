
import os
import network_type
from typing import Callable
from smallMITM import FakeClient,FakeServer

class MITM():

    def __init__(self):
        self.buffer_size      = 4096
        self.from_host        = '0.0.0.0' # all ip
        self.to_host          = '0.0.0.0' # all ip
        self.from_port        = 80
        self.to_port          = 80
        self.parse_function   = lambda x: x
        self.forward          = None
        self.network_type     = network_type.tcp

    def __repr__(self):
        dict = self.__dict__
        output = ""
        output += "MITM:\n\t".format(**dict)
        output += "\tbuffer_size: {buffer_size}\n".format(**dict)
        output += "\tfrom_host: {from_host}\n".format(**dict))
        output += "\tfrom_port: {port}\n".format(**dict)
        output += "\tto_host: {to_host}\n".format(**dict)
        output += "\tto_port: {to_port}\n".format(**dict)
        output += "\tnetwork_type: {network_type}\n".format(**dict)
        output += "\tdata parsing function: {parse_function}\n".format(**dict)
        output += "\tforwarder proxy: {forward}\n".format(**dict)
        return output

    def set_parse_function(self,function: Callable[[str],str]) -> MITM:
        self.set_parse_function(function)
        return self

    def set_from_host(self,from_host: str) -> MITM:
        self.from_host = from_host
        return self

    def set_from_port(self,from_port: int) -> MITM:
        self.from_port = from_port
        return self

    def set_to_host(self,to_host: str) -> MITM:
        self.to_host = to_host
        return self

    def set_to_port(self,to_port: int) -> MITM:
        self.to_port = to_port
        return self

    def set_buffer_size(self,buffer_size: int) -> MITM:
        self.buffer_size = buffer_size
        return self

    def start(self) -> None:
        try:
            self._start()
        except KeyboardInterrupt as e:
            print("Stopping the MITM")

    def _start(self) -> None:
        # create the two proxy
        fake_client = Fakeclient().set_buffer_size(self.buffer_size).set_parse_function(self.parse_function)
        fake_server = FakeServer().set_buffer_size(self.buffer_size).set_parse_function(self.parse_function)

        # cross link
        fake_client.set_fake_server(fake_server)
        fake_server.set_fake_client(fake_client)

        # setup the port and host
        fake_client.set_to_port(self.to_port).set_to_host(self.to_host)
        fake_server.set_from_port(self.from_port).set_from_host(self.from_host)

        fake_server.create()
        fake_client.create()

        fake_server.start()
        fake_client.start()

    def _exit_loop(self):
        while True:
            try:
                cmd = raw_input('$ ')
                if cmd[:4] == 'quit':
                    os._exit(0)
            except Exception as e:
                print e
