

class FakeClient():

    def __init__(self):
        self.fake_server      = None
        self.buffer_size      = 4096
        self.from_host        = '0.0.0.0' # all ip
        self.to_host          = '0.0.0.0' # all ip
        self.from_port        = 80
        self.to_port          = 80
        self.parse_function   = lambda x: x
        self.network_type     = network_type.tcp

    def set_buffer_size(self,buffer_size: int) -> FakeClient:
        self.buffer_size = buffer_size
        return self

    def set_parse_function(self,function: Callable[[str],str]) -> FakeClient:
        self.set_parse_function(function)
        return self

    def set_to_host(self,to_host: str) -> FakeClient:
        self.to_host = to_host
        return self

    def set_to_port(self,to_port: int) -> FakeClient:
        self.to_port = to_port
        return self

    def set_fake_server(self,fake_server: FakeServer) -> FakeClient:
        self.fake_server = fake_server
        return self

    def create(self) -> Proxy:
        self.send_socket = self.network_type.get_socket()
        self.send_socket.connect((self.to_host, self.to_port))

    def send(self,data) -> None:
        self.fake_server.send(data)

    def run(self) -> None:
        while True:
            self.accept_socket, addr = sock.accept()
            data = self.accept_socket.recv(self.buffer_size)
            if data:
                data = self.parse_function(data)
                # forward to client
                if(self.fake_server):
                    self.fake_server.send(data)
