#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,getpass

def login():
	# user = getpass.getuser() # 自动获取当前系统登录用户姓名
	user = input('Enter your username: ')
	print('User:',user)
	passwd = getpass.getpass() # Warning: Password input may be echoed. 弹出明文回应警告
	print('Passwd:',passwd)
	if (user,passwd) == ('tom','cat'):
		return True
	else:
		return False

if __name__=="__main__":
	try:
		if login():
			print('Welcome')
		else:
			print('Error')
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




