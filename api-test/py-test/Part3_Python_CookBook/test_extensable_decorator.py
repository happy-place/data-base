#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        借助装饰器，封装调用类型参数，丰富函数的调用方式
"""
import os,traceback,inspect
from functools import wraps


def optional_debug(func):
	@wraps(func)
	def wrapper(*args,debug=False,**kwargs):
		'''
		装饰器内部额外封装 debug参数，丰富调用方式，并且额外参数，可以通过目标函数代入
		感觉上好像是目标函数参数被扩充了，实质是该额外参数只对装饰器起作用
		
		通过装饰器可额外代入很多参数，具体王目标函数传入哪些参数取决于装饰器逻辑
		'''
		if debug:
			print('Calling ',func.__name__)
		return func(*args,**kwargs)
	return wrapper

@optional_debug
def spam(a,b,c):
	print(a,b,c)


def optional_debug1(func):
	'''
	@optional_debug1
	def bb(x,y,z,debug=True): # TypeError: debug argument already defined
	检测 被注解函数的入参中是否包含 debug ，如果包含会出现命名冲突问题，触发异常阻止
	'''
	print(inspect.getargspec(func).args)
	if 'debug' in inspect.getargspec(func).args:
		raise TypeError('debug argument already defined')
	
	@wraps(func)
	def wrapper(*args,debug=False,**kwargs): # 通过关键参数固定debug，要么不传，如果传入，必须在位置参数之后，键值对之前
		if debug:
			print('Calling ',func.__name__)
		return func(*args,**kwargs)
	return wrapper

@optional_debug1
def aa(x):
	pass

@optional_debug1
def bb(x,y,z):
	pass


# 命名冲突替换
def optional_debug2(func):
	if 'debug' in inspect.getargspec(func).args:
		raise TypeError('debug argument already defined')
	
	@wraps(func)
	def wrapper(*args, debug=False, **kwargs):
		if debug:
			print('Calling', func.__name__)
		return func(*args, **kwargs)
	
	sig = inspect.signature(func)
	parms = list(sig.parameters.values())
	# 被装饰函数，通过inspect 查看时，可以检测到装饰器内部封装了debug参数，就可以主动回避了
	parms.append(inspect.Parameter('debug',
	                               inspect.Parameter.KEYWORD_ONLY,
	                               default=False))
	wrapper.__signature__ = sig.replace(parameters=parms)
	return wrapper

@optional_debug2
def bbb(x,y,z):
	pass



if __name__=="__main__":
	try:
		# spam(1,2,3) # 1 2 3
		# spam(1,2,3,debug=True)
		'''
		Calling  spam
		1 2 3
		'''
		
		# aa(1)
		# bb(1,2,3)
		# bb(1,2,3,debug=True)
		
		print(inspect.signature(bbb)) # (x, y, z, *, debug=False)
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




