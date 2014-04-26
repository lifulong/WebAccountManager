#!/usr/bin/env	python
# -*- coding:utf-8 -*-


import crypto
import store
import binascii

class recorder:

	"""
		usr_key is an hash value of WebAccountManager usr passwd
	"""
	def __init__(self, key=None):
		self.key = key
		self.crypto = crypto.crypto_alg(key)
	
	def set_key(self, key):
		self.key = key
		self.crypto.set_key(key)
	
	def get_key(self):
		return self.key
	
	def mk_record(self, ower, account, alias, email, mobile, passwd=None):
		if passwd is None :
			raise ValueError
		self.ower = ower
		self.account = account
		self.alias = alias
		self.email = email
		self.mobile = mobile
		self.passwd = passwd
		self.to_ciphertext()
		return (self.ower, self.account, self.alias, self.email, self.mobile, self.enc_passwd)

	def gt_record(self, ower, account, alias, email, mobile, enc_passwd=None):
		if enc_passwd is None :
			raise ValueError
		self.ower = ower
		self.account = account
		self.alias = alias
		self.email = email
		self.mobile = mobile
		self.enc_passwd = enc_passwd
		self.to_plaintext()
		return (self.ower, self.account, self.alias, self.email, self.mobile, self.passwd)

	def to_plaintext(self):
		if self.enc_passwd is None:
			if self.passwd is None:
				raise ValueError
			return
		self.passwd = self.crypto.dec(binascii.a2b_hex(self.enc_passwd))

	def to_ciphertext(self):
		if self.passwd is None:
			if self.enc_passwd is None:
				raise ValueError
			return
		self.enc_passwd = binascii.b2a_hex(self.crypto.enc(self.passwd))

	def get_plain_record(self):
		if self.passwd is None and self.enc_passwd is not None:
			self.to_plaintext()
		return self.ower, self.account, self.alias, self.email, self.mobile, self.passwd
			

	def get_cipher_record(self):
		if self.enc_passwd is None and self.passwd is not None:
			self.to_ciphertext()
		return self.ower, self.account, self.alias, self.email, self.mobile, self.enc_passwd

	def enc_record(self, record):
		if type(record) is not tuple:
			raise TypeError
		enc_passwd = binascii.b2a_hex(self.crypto.enc(record[5]))
		return record[0], record[1], record[2], record[3], record[4], enc_passwd

	def dec_record(self, record):
		if type(record) is not tuple:
			raise TypeError
		passwd = self.crypto.dec(binascii.a2b_hex(record[5]))
		return record[0], record[1], record[2], record[3], record[4], passwd



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
		



if __name__ == '__main__':
	pass




