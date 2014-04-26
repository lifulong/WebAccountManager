#!/usr/bin/env	python
# -*- coding:utf-8 -*-

import hashlib

from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto import Random

class crypto_alg:

#key is an hash value of web account manager user passwd
	def __init__(self, key=None):
		self._key = key
		iv = Random.new().read(AES.block_size)
		self.cipher = AES.new(self._key, AES.MODE_ECB, iv)

#key is an hash value of web account manager user passwd
	def set_key(self, key):
		self._key = key
		iv = Random.new().read(AES.block_size)
		self.cipher = AES.new(self._key, MODE_ECB, iv)

	def enc(self, plain):
		if self._key is None:
			raise EmptyKeyError
		length = 16 - len(plain)%16
		while length != 0:
			plain += "\n"
			length -= 1
			
		return self.cipher.encrypt(plain)

	def dec(self, cipher):
		if self._key is None:
			raise EmptyKeyError
		return self.cipher.decrypt(cipher).rstrip('\n')

	def key(self, info):
		return info
	
def hash_usr_key(info):
	"""Used To Generate An Hash Verify Usr Login Passwd.

		Use SHA Alg.
	"""
	return hashlib.sha256(info).hexdigest()

def hash_key(info):
	"""Used To Generate An Hash For Usr Account Passwd Crpyto.

		Use MD5 Alg.
	"""
	return hashlib.md5(info).digest()


if __name__ == "__main__":
	pass


