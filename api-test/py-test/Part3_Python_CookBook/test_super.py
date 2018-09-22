#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

class A:
	def spam(self):
		print('A spam')
	
class B(A):
	def spam(self):
		print('B.spam')
		super().spam() # 存在继承关系，通过super() 调用到父类
 

def test_super1():
	b = B()
	b.spam()

class Base:
	def __init__(self):
		print('Base.__init__')
	
class AA(Base):
	def __init__(self):
		super().__init__()
		print('A.__init__')
	
	def hello(self):
		print('hello AA')
		super().hello()
	
	
class BB(Base):
	def __init__(self):
		super().__init__()
		print('B.__init__')
	
	def hello(self):
		print('hello world')
	
class CC(AA,BB):
	def __init__(self):
		super().__init__() # 确保父类对象先被创建
		print('C.__init__')

def test_mro():
	c = CC()
	'''
	Base.__init__
	B.__init__
	A.__init__
	C.__init__
	'''
	print(CC.mro())
	'''
	子类优先父类被检查，多个父类，依据其在MRO列表顺序被检查，属性同时存在多个父类，从左往右匹配
	[<class '__main__.CC'>, <class '__main__.AA'>, <class '__main__.BB'>, <class '__main__.Base'>, <class 'object'>]
	'''
	print(c.hello())
	'''
	hello AA
	hello world # AA hello() 中的super().hello() ,尽管Base 中没有 hello(),但此时将 BB 的 hello() 动态混入到Base,因此 AA 里面不报错
	None
	'''









if __name__=="__main__":
	try:
		# test_super1()
		test_mro()
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




