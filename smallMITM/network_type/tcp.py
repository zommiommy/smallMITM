
import socket
from .network_type import NetworkType

class TCP(NetworkType):
    def get_socket(self) -> socket.socket:
        return socket.socket(socket.AF_INET,socket.SOCK_STREAM)
