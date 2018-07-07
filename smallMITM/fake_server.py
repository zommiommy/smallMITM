

class FakeServer(Thread):

    def __init__(self):
        self.fake_client      = None
        self.buffer_size      = 4096
        self.from_host        = '0.0.0.0' # all ip
        self.to_host          = '0.0.0.0' # all ip
        self.from_port        = 80
        self.to_port          = 80
        self.parse_function   = lambda x: x
        self.emulate_src_port = False
        self.network_type     = network_type.tcp

    def set_buffer_size(self,buffer_size: int) -> FakeServer:
        self.buffer_size = buffer_size
        return self

    def set_parse_function(self,function: Callable[[str],str]) -> FakeServer:
        self.set_parse_function(function)
        return self

    def set_from_host(self,from_host: str) -> FakeServer:
        self.from_host = from_host
        return self

    def set_from_port(self,from_port: int) -> FakeServer:
        self.from_port = from_port
        return self

    def set_fake_client(self,fake_client: FakeClient) -> FakeServer:
        self.fake_client = fake_client
        return self

    def create(self)-> Proxy:
        self.listen_socket = self.network_type.get_socket()
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind((self.from_host, self.from_port))
        self.listen_socket.listen(1)

    def send(self,data) -> None:
        self.listen_socket.send(data)

    def run(self) -> None:
        while True:
            self.accept_socket, addr = sock.accept()
            data = self.accept_socket.recv(self.buffer_size)
            if data:
                data = self.parse_function(data)
                # forward to client
                if(self.fake_client):
                    self.fake_client.send(data)
