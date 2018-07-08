
from smallMITM import MITM

def my_parse_function(data: bytes,intro: str) -> bytes:
    with open("log.log","w")as f:
        f.write("{intro}: {data}\n\n".format(intro=intro,data=str(data)))
    return data

mitm = MITM().set_host("127.0.0.1").set_client_port(8888).set_server_port(9000).set_parse_function(my_parse_function)

print(mitm)

mitm.start()
