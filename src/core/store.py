#!/usr/bin/env	python
# -*- coding:utf-8 -*-


from config import *

if config.config_usr_info_storage is "sqlite":
	import sqlite_store as key_storage
elif config.config_usr_info_storage is "mysql":
	import mysql_store as key_storage
elif config.config_usr_info_storage is "file":
	import file_store as key_storage
else :
	import file_store as key_storage


class storage(key_storage.base_storage):

	def __init__(self, usr=None, usr_key=None):
		key_storage.base_storage.__init__(self, usr, usr_key)


if __name__ == '__main__':
	pass

