


0.0.0.1		2014.04.26  mosai  <msl.fulong@gmail.com>

* src directory
* src/core directory

* core.py: core file of WebAccountManager, provide interface for upper level use.
* crypto.py: provide enc,dec,hash interface for WebAccountManager, abstact detail enc/dec method
* store.py: provide usr account record storage method, abstract detail storage in use,
* file_store.py: use file as the usr account record storage
* sqlite_store.py: use sqlite sqlserver as the usr account record storage[not implement]
* mysql_store.py: use mysql sqlserver as the usr account record storage[not implement]
* auto_config.py: config file, config what kind of storage use, passwd store mode etc.[not implement]

* src/cli directory
* web_account_manager.py: an command line interface tool for user to manage his web account


* src/bs directory
* provide broswer interface tool for user to manage his web account[not implement]

* src/gui directory
* provide an gui tool for usr to manage his web account[not implement]

* src/test directory
* provide test script for WebAccountManager[not implement]

* src/tool directory
* provide debug/logging/config tool for WebAccountManager use[not implement]

* doc directory
* provide design description of the WebAccountManager


* This Version Design And Write In Less Than 8 Hours, There Is Plenty Of Room For Improment,
	Many Bugs Need To Solve.

