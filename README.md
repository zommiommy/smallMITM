### smallMITM

Easy to setup and configure package to do Man-In-The-Middle.
#### Example:
To setup the proxy that print the data that are exchanged and listen on port 9000 and forward everything to local host on port 8888 it's just as easy as:

```python

from smallMITM import MITM

def my_parse_function(data: bytes,intro: str) -> bytes:
    print(intro + str(data),end="\n\n")
    return data

mitm = MITM().set_host("127.0.0.1").set_client_port(8888).set_server_port(9000)
mitm.set_parse_function(my_parse_function)

print(mitm)
#MITM(0.0.0.0:9000 -> 127.0.0.1:8888):
#	buffer_size: 10485760
#	host: 127.0.0.1
#	client_port: 8888
#	server_port: 9000
#	network_type: <class 'smallMITM.network_type.tcp.TCP'>
# data parsing function: <function my_parse_function at 0x7fc6802a6e18>

mitm.start()
#[proxy(0.0.0.0:9000 -> 127.0.0.1:8888)] setting up
#[proxy(0.0.0.0:9000 -> 127.0.0.1:8888)] connection established
#[received from 127.0.0.1:8888]b"HTTP/1.1 200 OK\r\nServer: TornadoServer/5.0.2\r\nContent-Type:
image/vnd.microsoft.icon\r\nDate: Sun, 08 Jul 2018 08:56:40 GMT\r\nContent-Se ...

```

### Settings
The MITM Class follow the builder pattern so that you can set settings both like this:

```python
mitm = MITM()
mitm.set_buffer_size(1048576)
mitm.set_host("127.0.0.1")
mitm.set_client_port(8888)
mitm.set_server_port(9000)

```
or like this:

```python
mitm = MITM()
mitm.set_buffer_size(1048576).set_host("127.0.0.1").set_client_port(8888).set_server_port(9000)
```
 #### client_port
 It's the port of the destination of the data.
 
you can set it with:

```python
mitm.set_client_port(80)

```

#### BufferSize:
It's the dimension of the buffer that receive the data.
It's the parameter passed to line:
```python
data = self.accept_socket.recv(self.buffer_size)

```
you can change the receiver buffer size:

```python
mitm.set_buffer_size(1048576)

```
```
It also supports UDP:
```python

from smallMITM.network_type import UDP
mitm.set_network_type(UDP)

```

