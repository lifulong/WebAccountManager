
# 背景

	生活的现代化，使我们存在这各种各样的帐号，帐号中有帐号密码和口令；有些帐号我们并不经常使用，当需要登录的时候，我们可能会忘记密码，甚至忘记帐号。本帐号管理程序就是用户满足当今用户众多帐号管理的需求。

	本程序采用Python语言实现，数据加密采用AES算法，数据存储使用本地文件系统文件（后续可能支持Sqlite以及Mysql）。
	WebAccountManager

# 需求

	1. 可以存储帐号、别名、密码、帐号归属、绑定邮箱、绑定手机号、描述等
	2. 密码采用安全的AES加密，其他字段采用明文
	3. 加密存储部分的加密密码采用SHA1加密存储
	4. 有日志记录

# 总体设计

## 层次化、模块化设计

	1. 用户交互层（命令行、GUI、浏览器）
	2. 加密解密层（将用户信息，并将密码加密后一起交给数据存储层）
	3. 数据存储层（文件，各种数据库）
		
## 管理工具帐号密码存储

	1. 管理工具帐号口令规格化
		口令进行HASH运算后转化为32B十六进制字符串存储
	2. 多用户支持

## 调试输出可定制

##


# 密码文件设计

## 格式

	Owner	:	Account		:	Alias	:	Email	:	Mobile	:	Passwd
	BaiDu:leefulong:#:msl.fulong@gmail.com:18311092031:FE0ED8231224D3A1B8C71224D3A1B8C7
	TengXun:454574689:#:msl.fulong@gmail.com::FE0ED8231224D3A1B8C71224D3A1B8C7
	GitHub:msl.fulong@gmail.com:#:msl.fulong@gmail.com::FE0ED8231224D3A1B8C71224D3A1B8C7


