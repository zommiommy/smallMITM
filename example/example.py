
from smallMITM import MITM

def parse_function(data):
    print(type(data))
    print(data)
    return data


mitm = MITM().set_host("127.0.0.1").set_port(8888).set_parse_function(parse_function)

print(mitm)

mitm.start()
