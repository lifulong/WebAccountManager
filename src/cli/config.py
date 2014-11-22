#!/usr/bin/env	python
#! -*-coding-*-

import os.path as path

sys.path.append('../tool/')

from exception import *

class config(base_config):
	""" Parse config file and store it in class static value.
		
		Parse config value from json config file.
		Store config value in class.
	"""

	_debug = False
	_network_addr = "127.0.0.1"
	_network_port = 9444
	_network_iomodule = ASYNC
	_network_keepalive = False


	def parse_config(self):
		""" Parse config value and store it in config static value.

			May be overridden.
		"""

		val = self.get_value(["debug"])
		if val is not None:
			_debug = val

		val = self.get_value(["network", "address"])
		if val is not None:
			_network_addr = val

		val = self.get_value(["network", "port"])
		if val is not None:
			_network_port = val

		val = self.get_value(["network", "iomodule"])
		if val is not None:
			_network_iomodule = val

		val = self.get_value(["network", "keepalive"])
		if val is not None:
			_network_keepalive = val


def test():

	__config = config("_config.json")


if __name__ == "__main__":
	test()


