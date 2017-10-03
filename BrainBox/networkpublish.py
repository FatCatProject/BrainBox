import socket
from zeroconf import ServiceInfo
from zeroconf import Zeroconf


class NetworkPublish:
	def __init__(self, name="FatCatBB", port=8000):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		ip = socket.inet_aton(socket.gethostbyname(s.getsockname()[0]))
		s.close()

		self.info = ServiceInfo(
			type_="_{}._tcp.local.".format(name), name="_{}._tcp.local.".format(name), address=ip, port=port,
			properties={}, server=None
		)

		self.zc = Zeroconf()
		# TODO - Log this to systemlog
		self.zc.register_service(info=self.info, ttl=60)

	def __del__(self):
		# TODO - Log this to systemlog
		self.zc.unregister_service(self.info)
		# self.zc.close()  # TODO - Causes process to hang
		del self.zc
