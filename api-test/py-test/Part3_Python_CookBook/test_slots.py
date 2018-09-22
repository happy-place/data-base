#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

class Date:
	'''
	在类中定义 __slots__ 集合，可以收集类的属性字典，以更为紧凑方式存储类信息，节省内存，不利点在于不能添加额外属性了

	'''
	__slots__ = ['year','month','day']
	def __init__(self,year,month,day):
		self.year = year
		self.month = month
		self.day = day

class A:
	def __init__(self): # 双下划线开头 和 结尾，系统默认函数会属性，有特殊用途
		self._internal = 0
		self.public = 1
	
	def __hello(self): # 仅双下划线开头，被继承时，未区分会被重命名为 _A_hello
		print('A hello')
	
	def public_method(self): # 字母开头，公共属性 和 方法
		pass
	
	def _internal_method(self): # 下划线开头，私有属性 和 方法
		lambda_ = 2.0 # 与关键字冲突，使用后下划线替换

class B(A):
	def __init__(self):
		self.__private = 0
	
	def __hello(self): # 私有属性 和 方法避免被调用的原理是，将被重新命名为 _B__hello(),可被调用，但不让被显式调用
		print('B hello')



if __name__=="__main__":
	try:
	
		b = B()
		
		# b.__hello() # 无法访问
		b._B__hello() # B hello 私有属性 和 方法避免被调用的原理是，将被重新命名为 _B__hello(),可被调用，但不让被显式调用
	
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




