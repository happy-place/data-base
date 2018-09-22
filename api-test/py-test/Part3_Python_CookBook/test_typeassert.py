#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from inspect import signature
from functools import wraps



def typeassert(*ty_args,**ty_kwargs):
	def decorate(func):
		# ----- 装饰器实例化时执行一次 -------
		# 优化模式下，直接返回原型函数，不进行任何检查
		if not __debug__:
			return func
		
		# 获取装饰器的签名信息，统一收集列表ty_args 和 字典 ty_kwargs的类型约束信息，封装到 字典bound_types中
		sig = signature(func)
		bound_types = sig.bind_partial(*ty_args,**ty_kwargs).arguments
		print(bound_types) # OrderedDict([('x', <class 'int'>), ('y', <class 'int'>)])
		
		# ----- 装饰器每次被调用时执行一次 -------
		@wraps(func)
		def wrapper(*args,**kwargs):
			# 获取被装饰对象的 入参信息，统一封装到bound_values 字典
			bound_values = sig.bind(*args,**kwargs)
			print(bound_values) # <BoundArguments (x=1, y=2)>
			# 比对 入参类型是否 约束一致，不一致则报错
			for name,value in bound_values.arguments.items():
				if name in bound_types:
					if not isinstance(value,bound_types[name]):
						raise TypeError(
								'Argument {} must be {}'.format(name,bound_types[name])
								)
			return func(*args,**kwargs)
		return wrapper
	return decorate


@typeassert(int,int)
def add(x,y):
	return x + y


def test_add():
	'''
	add() 函数上的装饰器，明确指明了入参类型约束，此约束对所有的调用都适用
	:return:
	'''
	print(add(1,2))
	print(add(1,2.0)) # TypeError: Argument y must be <class 'int'>


@typeassert(int,z=int)
def spam(x,y,z=24):
	'''
	只对部分进行约束
	:param x:
	:param y:
	:param z:
	:return:
	'''
	print(x,y,z)
	
def test_spam():
	print(__debug__) # True
	spam(1,2,23)
	spam(1,'hello',23)

if __name__=="__main__":
	try:
		test_spam()
	
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




