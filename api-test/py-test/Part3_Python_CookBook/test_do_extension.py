#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

'''
借助装饰器扩展类 方法功能
'''
def log_getattribute(cls):
	# 获取被注释类的 __getattribute__ 函数
	orig_getattribute = cls.__getattribute__
	
	# 扩展
	def new_getattribute(self,name):
		print('getting ',name)
		return orig_getattribute(self,name)
	
	# 归还
	cls.__getattribute__ = new_getattribute
	return cls


@log_getattribute
class A:
	def __init__(self,x):
		self.x = x
	
	def spam(self):
		pass


def test_a():
	a = A(42)
	print(a.x)
	'''
	getting  x
	42
	'''
	
	print(a.spam())
	'''
	getting  spam
	None
	'''

# 通过继承扩展类方法的功能
class LoggedGetattribute:
	def __getattribute__(self, name):
		print('getting ',name)
		return super().__getattribute__(name)

class A(LoggedGetattribute):
	def __init__(self,x):
		self.x = x
	
	def spam(self):
		pass



if __name__=="__main__":
	try:
		test_a()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




