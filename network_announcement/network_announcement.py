import socket
from time import sleep

from zeroconf import ServiceInfo, Zeroconf

IP = socket.gethostbyname(socket.gethostname())
PORT = 9998  # TODO - Port number?

info = ServiceInfo(_type="_http._tcp.local.", name="FatCat BrainBox", address=IP, port=PORT, weight=0, priority=0,
	properties=None, server=None)

zeroconf = Zeroconf()

# TODO - Log this to systemlog

zeroconf.register_service(info)

try:
	while True:
		sleep(0.1)
except KeyboardInterrupt:
	pass
finally:
	# TODO - Log this to systemlog
	zeroconf.unregister_service(info)
	zeroconf.close()
