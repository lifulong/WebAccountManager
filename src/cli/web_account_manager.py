#!/usr/bin/env	python
# -*- coding:utf-8 -*-

import sys

sys.path.append("..")

from core import core

help_msg = """
	This Tool Is Used For Manage Your Web Account In Cmd Line.

	You should create a user first when you use this clint tool first time;
	And before you do anything with you account you should Login first.

	Copyright(C) 2014-   Lifl@XXXX.Inc
	Your Can Do Whatever You Want To Do With This SoftWare, No Copyright Reserved.
"""

choice_msg = """
	HHHHHH----------HHHHHH
	1. Create New User
	2. Login
	3. Logout
	4. Get Account Info
	5. Add Account Info
	6. Query Account Info
	7. Del Account Info
	8. Clear Account Info
	9. Del User
	h. Help
	q. Quit
	HHHHHH----------HHHHHH
"""

class cli_account_manager():

	def __init__(self):
		self._key_method_ = {
			'1'	: self.create_user,
			'2'	: self.login,
			'3'	: self.logout,
			'4'	: self.get_account_info,
			'5'	: self.add_account_info,
			'6'	: self.query_account_info,
			'7'	: self.del_account_info,
			"h" : self.help_info,
			'q' : self.quit,
		}
		self.account_manager = None

	def create_user(self):
		self.account_manager = core.web_account_manager()
		usr = raw_input("Please Input Your User Name, And Press <Enter>:")
		usr_key = raw_input("Please Input Your Pass Word, And Press <Enter>:")
		self.account_manager.create_manager_usr(usr, usr_key)
		print "Create One New User:{0},UsrKey:{1}".format(usr, usr_key)

	def login(self):
		usr = raw_input("Please Input Your User Name, And Press <Enter>:")
		usr_key = raw_input("Please Input Your Pass Word, And Press <Enter>:")
		if self.account_manager is None:
			self.account_manager = core.web_account_manager(usr, usr_key)
		else:
			print "Usr:{0} has login, You Must Logout First.".format(self.account_manager.get_usr())
			return
		print "Usr:{0} Login Ok.".format(usr)

	def logout(self):
		if self.account_manager is None:
			print "You Must Login First."
			return
		self.account_manager = None;

	def get_account_info(self):
		if self.account_manager is None:
			print "You Must Login First."
			return
		records = self.account_manager.get_records()
		print "#{0}\t:\t{1}\t:\t{2}\t:\t{3}\t:\t{4}\t:\t{5}\n". \
				format("Ower", "Account", "Alias", "Email", "Mobile", "Passwd")
		for record in records:
			print "{0}:{1}:{2}:{3}:{4}:{5}\n".format(record[0], record[1], record[2], record[3], record[4], record[5])

	def add_account_info(self):
		if self.account_manager is None:
			print "You Must Login First."
			return
		ower = raw_input("Please Input Where Your New Account Belog To, And Press <Enter>:")
		account = raw_input("Please Input Your New Account Name, And Press <Enter>:")
		alias = raw_input("Please Input Your New Account Alias, And Press <Enter>:")
		email = raw_input("Please Input Your New Account Register Email, And Press <Enter>:")
		mobile = raw_input("Please Input Your New Account Register Mobile, And Press <Enter>:")
		passwd = raw_input("Please Input Your New Account Passwd, And Press <Enter>:")
		self.account_manager.append_record(ower=ower, account=account, alias=alias, email=email, mobile=mobile, passwd=passwd)
		print "Add New Account Ok."

	def query_account_info(self, query_string):
		if self.account_manager is None:
			print "You Must Login First."
			return
		if self.account_manager.has_attr(query_records):
			self.account_manager.query_records(query_string)
		pass

	def del_account_info(self, del_string):
		if self.account_manager is None:
			print "You Must Login First."
			return
		pass

	def help_info(self):
		print help_msg

	def quit(self):
		sys.exit()

	def run(self):
		print help_msg
		while True:
			print choice_msg
			choice = raw_input("Please Input Your Choice Charator,Then Press <Enter>:")
			self._key_method_[choice]()

if __name__ == '__main__':
	manager = cli_account_manager()
	manager.run()
	

