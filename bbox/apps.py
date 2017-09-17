from django.apps import AppConfig


class BboxConfig(AppConfig):
	name = 'bbox'

	def ready(self):
		import socket
		from zeroconf import ServiceInfo
		from zeroconf import Zeroconf
		ip = socket.inet_aton(socket.gethostbyname(socket.gethostname()))
		port = 9998  # TODO - Port number?
		info = ServiceInfo(
			type_="_FatCatBB._tcp.local.", name="_FatCatBB._tcp.local.", address=ip, port=port, properties={},
			server=None
		)
		zeroconf = Zeroconf()
		# TODO - Log this to systemlog
		zeroconf.register_service(info)

	# zeroconf.unregister_service(info)
	# zeroconf.close()
