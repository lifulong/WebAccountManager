#!/usr/bin/env	python
# -*- coding:utf-8 -*-


import json as parser

#from exception import *

class config :
	""" Load config file & Parse & Store it.

		parse config value from config file;
		get config value from parsed config value.
	"""


	""" Storage alternatives is file, sqlite, mysql, nosql;
		file is impied term;
	"""
	config_usr_info_storage = "file"

	config_tcp_svr_addr = "*"
	config_tcp_svr_port = 9444

	def __init__(self, _file):

		if _file is None:
			raise ConfigErr
		with open(_file) as __file:
			self.config_value = parser.load(__file)
			if __debug__:
				print "ConfigValue:", (type(self.config_value), self.config_value)
				print

		self.parse_config()

	def _get_value(self, config_value, keys):
		""" Parse value from * use keys.
			Return dict,tuple,list,str,num.
		"""

		if __debug__ :
			if config_value is not None:
				print "config_value:", config_value
			if keys is not None and len(keys) != 0:
				print "keys:", keys

		if config_value is None:
			return None
		if keys is None or len(keys) == 0:
			return None

		key = keys[0]
		reserv_keys = keys[1:]

		if type(config_value) is dict:
			cfg_value = config_value[key]
		else :
			return None

		if len(reserv_keys) == 0:
			return cfg_value

		if type(cfg_value) is not dict :
			return None

		return self._get_value(cfg_value, reserv_keys)

	def get_value(self, keys):
		""" Return dict,tuple,list,str,num.
		"""

		return self._get_value(self.config_value, keys)

	def parse_config(self):
		""" Parse config value and store it in config static value.
		"""

		ip_addr = self.get_value(["svr_addr", "ip_addr"])
		if ip_addr is not None:
			if ip_addr == "*":
				config.config_tcp_svr_addr = ""
			else :
				config.config_tcp_svr_addr = ip_addr

		ip_port = self.get_value(["svr_addr", "ip_port"])
		if ip_port is not None:
			config.config_tcp_svr_port = int(ip_port)

		storage_type = self.get_value(["storage", "type"])
		if storage_type is not None:
			config.config_usr_info_storage = storage_type

		if __debug__ :
			print config.config_tcp_svr_addr, config.config_tcp_svr_port, config.config_usr_info_storage


if __name__ == "__main__":
	__config = config("_config.json")


