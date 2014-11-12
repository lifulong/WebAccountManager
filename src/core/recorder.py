#!/usr/bin/env	python

"""
	class recorder provide the method to deal record of account-manager

	dec enc methon for example
"""

import crypto
import binascii

class recorder:
	"""
		key is an hash value of account-manager usr passwd
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



