
#!/usr/bin/env	python

__all__ = ['UsrError', 'PasswdError', 'LoginError', 'EmptyKeyError']

class UsrError(Exception):
	"""Exception raised by user not valid."""
	pass

class PasswdError(Exception):
	"""Exception raised by user passwd not valid."""
	pass

class LoginError(Exception):
	"""Exception raised while user not login Or create new usr while login."""
	pass

class EmptyKeyError(Exception):
	"""Exception raised by has no key while crypto."""
	pass


