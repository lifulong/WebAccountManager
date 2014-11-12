#!/usr/bin/env	python
# -*- coding:utf-8 -*-


from recorder import *
import store
import binascii

class web_account_manager:

	def __init__(self, usr=None, passwd=None):
		#Check user valid
		if passwd is not None:
			usr_key = crypto.hash_usr_key(passwd)
			key = crypto.hash_key(passwd)
		else:
			usr_key = None
			key = None
		self.storage = store.storage(usr, usr_key)
		self.recorder = recorder(key)
		self.usr = usr
		self.usr_key = usr_key
		self.key = key

	def get_manager_usr(self):
		""" Get The Manager User Login, And Return It.

			this method is used for check who has been login.
		"""
		return self.usr

	def get_manager_usr_key(self):
		""" Get The Manager User Passwd, And Return It.

			the passwd is used for the user login in the pass word manager, and 
			used to enctrypt the pass word segment of the user account info.
		"""
		key = self.storage.get_usr_key()
		return key

	def verify_manager_usr_key(self, passwd):
		key = get_manager_usr_key()
		hash_key = crpyto.hash_usr_key(passwd)
		if key is not hash_key:
			return False
		return True

	def create_manager_usr(self, usr, usr_key):
		if usr_key is not None:
			hash_key = crypto.hash_usr_key(usr_key)
		self.storage.new_user(usr, hash_key)
	
	def delete_manager_usr(self, usr):
		pass

	def get_usr_records(self):
		""" Inner Interface
		"""
		return self.storage.get_records()

	def get_records(self):
		"""Used To Get All Account Info, Which Show To User.
		"""
		records = self.get_usr_records()
		dec_records = []
		for record in records:
			record = self.recorder.dec_record(record)
			dec_records.append(record)
		return dec_records
	
	def append_record(self, **kwargs):
		if kwargs.has_key("ower"):
			ower = kwargs["ower"]
		else:
			ower = ""
		if kwargs.has_key("account"):
			account = kwargs["account"]
		else:
			account = ""
		if kwargs.has_key("alias"):
			alias = kwargs["alias"]
		else:
			alias = ""
		if kwargs.has_key("email"):
			email = kwargs["email"]
		else:
			email = ""
		if kwargs.has_key("mobile"):
			mobile = kwargs["mobile"]
		else:
			mobile = ""
		if kwargs.has_key("passwd"):
			passwd = kwargs["passwd"]
		else:
			passwd = ""
		record = self.recorder.mk_record(ower, account, alias, email, mobile, passwd)
		self.storage.append_record(record)
		
	def query_records(self, query_string):
		"""
		"""
		pass

	def del_records(self, del_string):
		pass



if __name__ == '__main__':
	pass




