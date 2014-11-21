#!/usr/bin/env	python

"""
	class record provide the method to deal with record of account-manager user

	dec enc record method for example
"""

import crypto
import binascii

class record:
	""" Record of account-manager.

	"""

	def __init__(self, key=None):
		"""
			key is an hash value of account-manager usr passwd
		"""
		self.key = key
	
	def set_key(self, key):
		self.key = key
	
	def get_key(self):
		return self.key

	def to_plaintext(self):
		""" Decrpt passwd from encrpt passwd.
		"""

		if self.enc_passwd is None:
			if self.passwd is None:
				raise ValueError
			return
		self.passwd = crypto.dec(binascii.a2b_hex(self.enc_passwd))

	def to_ciphertext(self):
		""" Encrpt passwd from decrpt passwd.
		"""

		if self.passwd is None:
			if self.enc_passwd is None:
				raise ValueError
			return
		self.enc_passwd = binascii.b2a_hex(self.crypto.enc(self.passwd))

	def mk_record(self, ower, account, alias, email, mobile, passwd=None):
		""" Make encrpt account-manager record info by usr input info & Return it.
		"""

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
		""" Get decrpt account-manager record from encrpt record info & Return it.
		"""

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

	def enc_record(self, record):
		""" Encrpt input record & Return it.
		"""

		if type(record) is not tuple:
			raise TypeError
		enc_passwd = binascii.b2a_hex(crypto.enc(record[5]))

		return record[0], record[1], record[2], record[3], record[4], enc_passwd

	def dec_record(self, record):
		""" Decrpt input record & Return it.
		"""

		if type(record) is not tuple:
			raise TypeError
		passwd = crypto.dec(binascii.a2b_hex(record[5]))

		return record[0], record[1], record[2], record[3], record[4], passwd

	def get_plain_record(self):
		""" Get plain record from record info.
		"""

		if self.passwd is None and self.enc_passwd is not None:
			self.to_plaintext()

		return self.ower, self.account, self.alias, self.email, self.mobile, self.passwd
			

	def get_cipher_record(self):
		""" Get cipher record from record info.
		"""

		if self.enc_passwd is None and self.passwd is not None:
			self.to_ciphertext()

		return self.ower, self.account, self.alias, self.email, self.mobile, self.enc_passwd



