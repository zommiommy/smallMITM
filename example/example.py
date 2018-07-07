
from smallMITM import MITM
import dinamic_library

def parse_function(data):
    reload(dinamic_library)
    return dinamic_library.parse_function(data)

MITM().set_to_host('192.168.178.54').set_port(3333).set_parse_function(parse_function).start()
