#!/usr/bin/env	python
# -*- coding:utf-8 -*-

"""

"""

from exception import *

class base_storage:

	def __init__(self, usr=None, usr_key=None):
		self.usr_key = None
		self.usr = None
		self.records = []
		if usr is None:
			return
		self.load_info_from_file()
		if self.usr != usr:
			raise UsrError
		if self.usr_key != usr_key:
			raise PasswdError

	def new_user(self, usr, usr_key):
		"""
			create or register new user to file storage
		"""
		if self.usr is not None:
			raise LoginError, "Login In Usr Can Not Create New Usr,You Should Logout First."
		self.usr = usr
		self.usr_key = usr_key
		self.flush_all()

	def load_info_from_file(self, filename="passwd"):
		"""
			load and parse usr-passwd and usr account info
		"""
		with open(filename) as f:
			for line in f:
				line = line.strip('\n')
				if line is "" or line.startswith("#") or line.startswith('"""'):
					continue
				if self.parse_manager_usr_info(line):
					continue
				else:
					record = self.parse_manager_record(line)
					self.records.append(record)

		if self.usr is None or self.usr_key is None:
			raise UsrError

	def parse_manager_usr_info(self, info_str):
		"""
			parse account-manager usr info to usr and passwd
		"""

		info_list = info_str.split(":")
		if len(info_list) is not 2:
			return False
		else:
			if info_list[0] == "usr":
				self.usr = info_list[1]
			elif info_list[0] == "key":
				self.usr_key = info_list[1]
				if len(self.usr_key) is not 64:
					raise ValueError
			else:
				return False
			return True

	def parse_manager_record(self, info_str):
		"""
			parse one record string to record tuple
		"""

		info_list = info_str.split(":")
		if len(info_list) is not 6:
			return None
		return info_list[0], info_list[1], info_list[2], info_list[3], info_list[4], info_list[5]

	def get_usr_info(self, usr=None):
		"""Export interface
		"""
		return self.usr, self.usr_key

	def get_usr_key(self, usr=None):
		"""Export interface
		"""
		return self.usr_key

	def get_records(self):
		"""Export interface
		"""
		return self.records

	def flush_one_record(self, record):
		"""
			append one record to record file
		"""
		with open("passwd", "a+") as f:
			f.write("{0}:{1}:{2}:{3}:{4}:{5}\n".format(record[0], record[1], record[2], record[3], record[4], record[5]))
			

	def flush_all(self):
		"""
			flush usr&passwd and account record info to record file
		"""
		with open("passwd", "w+") as f:
			if self.usr is not None:
				f.write("usr:{0}\n".format(self.usr))
			if self.usr_key is not None:
				f.write("key:{0}\n".format(self.usr_key))
			f.write("#{0}\t:\t{1}\t:\t{2}\t:\t{3}\t:\t{4}\t:\t{5}\n".
					format("Ower", "Account", "Alias", "Email", "Mobile", "Passwd"))
			for record in self.records:
				f.write("{0}:{1}:{2}:{3}:{4}:{5}\n".format(record[0], record[1], record[2], record[3], record[4], record[5]))
	
	
	def set_usr_info(self, info):
		"""Export interface
			set usr&key to account info storage
		"""
		if type(info) is not tuple:
			raise TypeError
		if len(info) is not 2:
			raise ValueError
		self.usr = info[0]
		self.usr_key = info[1]
		self.flush_all()

	def set_key(self, key):
		"""Export interface
			set usr key to account info storage
		"""
		if self.usr is None:
			raise UsrError, "Usr Is None."
		if type(key) is not str:
			raise TypeError
		if key is None:
			raise ValueError
		self.usr_key = key
		self.flush_all()

	def put_record(self, record):
		"""Export interface
		"""
		if record is not tuple:
			raise TypeError
		if len(record) is not 6:
			raise ValueError
		self.records.append(record)
		self.flush_all()

	#Check repeat
	def append_record(self, record):
		"""Export interface
		"""
		if type(record) is not tuple:
			raise TypeError
		if len(record) is not 6:
			raise ValueError
		self.records.append(record)
		self.flush_one_record(record)

	def put_records(self, records):
		pass

	def append_records(self, records):
		if type(records) is not list:
			raise TypeError
		for record in records:
			if type(record) is not tuple:
				raise TypeError
			if len(record) is not 6:
				raise ValueError
			self.records.append(record)
			self.flush_one_record(record)



if __name__ == '__main__' :
	pass



