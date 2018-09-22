#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        自定义异常类应该总是继承自内置的 Exception 类， 或者是继承自那些本身就是从 Exception 继承而来的类。
        尽管所有类同时也继承自 BaseException ，但你不应该使用这个基类来定义新的异常。 BaseException 是为系统退出异常而保留的，
        比如 KeyboardInterrupt 或 SystemExit 以及其他那些会给应用发送信号而退出的异常。 因此，捕获这些异常本身没什么意义。
         这样的话，假如你继承 BaseException 可能会导致你的自定义异常不会被捕获而直接发送信号退出程序运行。
"""
import os,traceback

class NetworkError(Exception):
	pass

class HostnameError(NetworkError):
	pass

class TimeoutError(NetworkError):
	pass

class ProtocolError(NetworkError):
	pass

class CustomerError(Exception):
	def __init__(self,msg,status):
		# 复写 __init__ 函数时，需要调用super().__init()保证父类参数也被重新实例化
		super().__init__(msg,status)
		self.msg = msg
		self.status = status

def test_customer():
	try:
		raise CustomerError('customer error',20)
	except Exception as e:
		print(e.msg,e.status)
		print(e.args)

def test_args():
	'''
	. 很多其他函数库和部分Python库默认所有异常都必须有 .args 属性， 因此如果你忽略了这一步，
	你会发现有些时候你定义的新异常不会按照期望运行。
	'''
	try:
		raise RuntimeError('It failed',43,'spam')
	except RuntimeError as e:
		print(e.args)
		




if __name__=="__main__":
	try:
		# test_customer()
		test_args()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




