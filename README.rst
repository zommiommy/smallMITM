.. role:: py(code)
   :language: python

smallMITM
==========

|travis| |coveralls| |sonar_quality| |sonar_maintainability| |code_climate_maintainability| |code_climate_test_coverage| |pip|

Easy to setup and configure package to do Man-In-The-Middle.

Basic Example:
--------------
To setup the proxy that print the data that are exchanged and listen on port 9000 and forward everything to local host on port 8888 it's just as easy as:

.. code:: python

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
	#image/vnd.microsoft.icon\r\nDate: Sun, 08 Jul 2018 08:56:40 GMT\r\nContent-Se ...


The Example:
--------------
If you modify slightly the parse_function the MITM can became really powerful.
If you define the function in a different file like myfunction.py you can import it and using the
reload built-in function you can reload the file.
This allow to modify the parse_function live without having to restart the MITM

.. code:: python

	import myfunction

	def my_parse_function(data: bytes,intro: str) -> bytes:
	    reload(myfunction)
	    return myfunction.myfunction(data,intro)



Settings
--------------
The MITM Class follow the builder pattern so that you can set settings both like this:

.. code:: python

	mitm = MITM()
	mitm.set_buffer_size(1048576)
	mitm.set_host("127.0.0.1")
	mitm.set_client_port(8888)
	mitm.set_server_port(9000)


or like this:

.. code:: python

	mitm = MITM()
	mitm.set_buffer_size(1048576).set_host("127.0.0.1").set_client_port(8888).set_server_port(9000)

parse_function
--------------
It's the function that take the incoming data and return it to be forwarded.
It take 2 arguments, the data in bytes and the intro which is a string in the form
"127.0.0.1:8888" to know from where the data is comming.

.. code:: python

	def my_parse_function(data: bytes,intro: str) -> bytes:
	    print(intro + str(data),end="\n\n")
	    return data

	mitm.set_parse_function(my_parse_function)


network_type
--------------
The network protocol of the MITM, it currently support both TCP and UDP. TCP is setted as default.

.. code:: python

	from smallMITM.network_type import TCP
	mitm.set_network_type(TCP)

	from smallMITM.network_type import UDP
	mitm.set_network_type(UDP)


server_port
--------------
It's the port on which the MITM will be listening for clients.
you can set it with:


.. code:: python

	mitm.set_server_port(8888)



host
--------------
It's where the ip of the destination of the data


.. code:: python

	mitm.set_host("192.168.1.6")


client_port
--------------
It's the port of the destination of the data.
you can set it with:


.. code:: python

	mitm.set_client_port(80)



buffer_size:
--------------
It's the dimension of the buffer that receive the data.
It's the parameter passed to line:

.. code:: python

	data = self.accept_socket.recv(self.buffer_size)


you can change the receiver buffer size:


.. code:: python

	mitm.set_buffer_size(1048576)


.. |travis| image:: https://travis-ci.org/zommiommy/smallMITM.png
   :target: https://travis-ci.org/zommiommy/smallMITM

.. |coveralls| image:: https://coveralls.io/repos/github/zommiommy/smallMITM/badge.svg?branch=master
    :target: https://coveralls.io/github/zommiommy/smallMITM

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=dictances.lucacappelletti&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/dictances.lucacappelletti

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=dictances.lucacappelletti&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/dictances.lucacappelletti

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/5ffb5f7af34008c78e2c/maintainability
   :target: https://codeclimate.com/github/zommiommy/smallMITM/maintainability
   :alt: Maintainability

.. |code_climate_test_coverage| image:: https://api.codeclimate.com/v1/badges/5ffb5f7af34008c78e2c/test_coverage
   :target: https://codeclimate.com/github/zommiommy/smallMITM/test_coverage
   :alt: Test Coverage


.. |pip| image:: https://badge.fury.io/py/dictances.svg
    :target: https://badge.fury.io/py/dictances
