#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,types
from functools import wraps

class A:
	# 基于A 实例装饰器
	def decorate1(self,func):
		@wraps(func)
		def wrapper(*args,**kwargs):
			print('Decorator 1')
			return func(*args,**kwargs)
		return wrapper
	
	# 基于A类装饰器
	@classmethod
	def decorate2(cls,func):
		@wraps(func)
		def wrapper(*args,**kwargs):
			print('Decorator 2')
			return func(*args,**kwargs)
		return wrapper


a = A()
@a.decorate1
def spam():
	pass

@A.decorate2
def grok():
	pass


def test_a():
	spam() # Decorator 1
	grok() # Decorator 2
	

class Profiled:
	def __init__(self,func):
		wraps(func)(self)
		self.ncalls = 0
	
	def __call__(self,*args,**kwargs):
		self.ncalls +=1
		return self.__wrapped__(*args,**kwargs)
	
	def __get__(self,instance,cls):
		if instance is None:
			return self
		else:
			return types.MethodType(self,instance)
	
	
# 修饰函数 __call__ 起作用
@Profiled
def add(x,y):
	return x + y

# 修饰方法 __get__ 起作用
class Spam:
	@Profiled
	def bar(self,x):
		print(self,x)


# 通过闭包和nocalls变量实现装饰器
def profiled(func):
	ncalls = 0
	@wraps(func)
	def wrapper(*args,**kwargs):
		nonlocal ncalls
		ncalls +=1
		return func(*args,**kwargs)
	
	# 属性绑定到方法上
	wrapper.ncalls = lambda :ncalls
	
	return wrapper


@profiled
def addition(x,y):
	return x+y


if __name__=="__main__":
	try:
		# # test_a()
		# add(2,3)
		# add(4,5)
		# print(add.ncalls) # 2 被调用了两次
		#
		# s = Spam()
		# s.bar(1) # <__main__.Spam object at 0x102a16400> 1
		# s.bar(2) # <__main__.Spam object at 0x102a16400> 2
		# print(Spam.bar.ncalls) # 2 被调用了两次
		
		addition(1,2)
		addition(1,2)
		print(addition.ncalls()) # 2
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




