#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,time
from functools import wraps
from abc import ABCMeta,abstractmethod


def timethis(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		start = time.time()
		r = func(*args,**kwargs)
		end = time.time()
		print(end-start)
		return r
	return wrapper

class Spam:
	''' 装饰器修饰实例方法，类方法，静态方法
	默认类方法 和 静态方法不会直接返回可调用对象因此，装饰器 @timethis 注解需要摆在最内侧
	'''
	
	@timethis
	def instance_method(self,n):
		print(self,n)
		while n >0:
			n -= 1
	
	@classmethod
	@timethis
	def class_method(cls,n):
		print(cls,n)
		while n >0:
			n -= 1
	
	@staticmethod
	@timethis
	def static_method(n):
		print(n)
		while n >0:
			n -= 1


def test_spam():
	s = Spam()
	s.instance_method(10) # <__main__.Spam object at 0x10489afd0> 10
	Spam.class_method(10) # <class '__main__.Spam'> 10
	Spam.static_method(10) # 10
	

# 声明接口时，需要将@abstractmethod注解写在最内侧
class AA(metaclass=ABCMeta):
	@classmethod
	@abstractmethod
	def method(cls):
		pass







if __name__=="__main__":
	try:
		test_spam()
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




