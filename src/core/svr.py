#!/usr/bin/env	python
# -*- coding:utf-8 -*-

"""
This file implement the tcp server for account-manager.

Multi Thread.
"""

from config import *
from socket_svr import *

class RequestHandlerClass(StreamRequestHandler):

	def __init__(self):
		pass

class svr(ThreadingTCPServer):
	""" TCP Svr of account-manager.
	"""

	def __init__(self):

		self._config = config("_config.json")
		address = (config.config_tcp_svr_addr, config.config_tcp_svr_port)

		if __debug__ :
			print "Address is %s:%d.", address

		#supper(svr, self).__init__(self)
		ThreadingTCPServer.__init__(self, address, RequestHandlerClass)

		self.start()

	def run(self):

		print "Svr running."
	
	def start(self):

		self.run()


if __name__ == '__main__':

	account_manager_svr = svr()


