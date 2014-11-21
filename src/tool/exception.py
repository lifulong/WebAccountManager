#!/usr/bin/env	python

__all__ = ['UsrError', 'PasswdError', 'LoginError', 'KeyError', 'EmptyKey']

class UsrError(Exception):
	"""Exception raised by user not valid."""
	pass

class PasswdError(Exception):
	"""Exception raised by user passwd not valid."""
	pass

class LoginError(Exception):
	"""Exception raised while user not login Or create new usr while login."""
	pass

class KeyError(Exception):
	"""Exception raise while input an error key.
	"""
	pass

class EmptyKey(KeyError):
	"""Exception raise while input an empty key.
	"""
	pass


