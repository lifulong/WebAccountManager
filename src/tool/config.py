#!/usr/bin/env	python
#! -*-coding-*-

import sys
import json as parser
import os.path as path

from exception import *

class base_config:
	""" Parse config file and store it in class static value.
		
		Parse config value from json config file.
		Store config value in class.
	"""

	_debug = False

	def __init__(self, _file):

		if _file is None:
			return

		if not path.isfile(_file):
			raise ConfigError

		self.load(_file)


	def load(self, _file):

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

			May be overridden.
		"""

		pass

def test():

	config = base_config("_test_config.json")
	_comment = config.get_value(["_comment"])
	if _comment is not None:
		print "_comment:", _comment

if __name__ == "__main__":
	test()


