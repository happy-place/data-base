#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
	你想在函数上添加一个包装器，增加额外的操作处理(比如日志、计时等)。
"""
import os,traceback
import time
from functools import wraps
from inspect import signature


def timethis(func):
	# @wraps(func) # 带上 此注解会多包一层，花费时间更多，但可以充分保留原始函数的元数据信息
	def wrapper(*args,**kwargs):
		start = time.time()
		result = func(*args,**kwargs)
		end = time.time()
		print(func.__name__,end-start)
		return result
	return wrapper

def timethis1(func):
	@wraps(func) # 带上 此注解会多包一层，花费时间更多，但可以充分保留原始函数的元数据信息
	def wrapper(*args,**kwargs):
		start = time.time()
		result = func(*args,**kwargs)
		end = time.time()
		print(func.__name__,end-start)
		return result
	return wrapper

@timethis
def countdown(n:int):
	'''
	do count
	'''
	while n > 0:
		n -= 1


@timethis1
def countdown1(n:int):
	'''
	do count
	'''
	while n > 0:
		n -= 1


def do_sleep(n):
	time.sleep(n)


def test_wraps():
	countdown(10) # countdown 4.0531158447265625e-06
	countdown1(10) # countdown1 2.1457672119140625e-06

	# countdown() 函数上使用了@timethis 注解，此注解在包装函数时，没有使用 @wraps(func) 注解，因此会丢失被包装函数 func 的元数据信息
	print(countdown.__name__,countdown.__doc__,countdown.__annotations__)
	'''
	wrapper None {}
	'''
	
	# countdown() 函数上使用了@timethis1 注解，此注解在包装函数时，使用 @wraps(func) 注解，因此不会丢失被包装函数 func 的元数据信息
	# 并且运行至今通过 func.__wrapped__() 形式访问被包装的函数
	print(countdown1.__name__,countdown1.__doc__,countdown1.__annotations__)
	'''
	countdown1 函数名
	do count  函数文档
	 {'n': <class 'int'>} 注释
	'''
	
	# 被装饰器注释的函数countdown1,通过 __wrapped__() 函数直接，解除装饰器，实现对原函数的访问
	orgi_countdown1 =countdown1.__wrapped__
	orgi_countdown1(10)
	
	# 装饰器内部使用 了@wraps 注解时，运行直接通过 signature 获取被包装函数的签名信息
	print(signature(countdown)) # (*args, **kwargs)
	print(signature(countdown1)) # (n:int)
	


class A:
	'''
	类内置装饰器：@staticmethod,@classmethod,@property，
	所有内置装饰器没有使用 @wraps 修饰，直接将函数信息存储在 __func__中
	'''
	@classmethod #
	def method1(cls):
		pass
	
	def method2(cls):
		pass
	
	method2 = classmethod(method2) # 与上面使用注解效果一致，都声明了类方法





if __name__=="__main__":
	try:
		# # 使用注解
		# countdown(100) # countdown 1.4066696166992188e-05
		#
		# # 直接包装函数
		# wp = timethis(do_sleep)
		# wp(3) # do_sleep 3.0043509006500244
		
		test_wraps()
		
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




