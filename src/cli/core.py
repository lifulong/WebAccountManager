#!/usr/bin/env	python
#! -*-coding-*-


class web_account_manager:
	""" AM(Web Account Manager).

		Provide interface to deal usr input.
		Transfer data with account-manager tcp server.
	"""

	def __init__(self, svr_address, keep_alive=False, iomodule="async"):

		self._socket = None
		self.is_alive = False

		if keep_alive:
			try:
				self._socket = socket.socket(AF_INET, SOCK_STREAM, 0)
				self._socket.connect(svr_address)
				self.rfile = self._socket.makefile("rb")
				self.wfile = self._socket.makefile("wb")
				self.is_alive = True
			except:
				self._socket = None
				self.is_alive = False

	def send_header(self):
		""" Send header to peer server.

			Write header info to socket wfile.
		"""
		pass

	def send_head(self):
		pass


	def get_value(self):
		""" Parse json response.

			Return dict.
		"""
		pass

	def make_request(self):
		pass

	def handle_command(self, cmd, **kwargs):
		""" handle one usr command.

			Support Async IO Module, cmd & command_dict required by this method.
		"""

		json_str = json.dumps(kwargs, sort_keys=True, separater=(',', ':'))
	
	def register(self, usr, email, passwd):

		self.usr = usr
		command_dict["usr"] = usr
		command_dict["email"] = email
		command_dict["passwd"] = passwd
		self.handle_command("REGISTER", command_dict)
		command_dict.clear()

	def login(self, usr, passwd):
		pass

	def logout(self, usr):
		pass

	def get_records(self, usr):
		pass

	def put_records(self, usr):
		pass

	def del_records(self, usr):
		pass

	def mod_record(self, usr):
		pass


