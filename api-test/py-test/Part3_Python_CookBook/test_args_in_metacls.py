#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from abc import ABCMeta,abstractmethod

class IStream(metaclass=ABCMeta):
	@abstractmethod
	def read(self,maxsize=None):
		pass
	
	@abstractmethod
	def write(self,data):
		pass


class MyMeta(type):
	'''
	__prepare__() 方法在所有类定义开始执行前首先被调用，用来创建类命名空间。 通常来讲，这个方法只是简单的返回一个字典或其他映射对象。
	__new__() 方法被用来实例化最终的类对象。它在类的主体被执行完后开始执行。
	__init__() 方法最后被调用，用来执行其他的一些初始化工作。
	
	当我们构造元类的时候，通常只需要定义一个 __new__() 或 __init__() 方法，但不是两个都定义。
	但是，如果需要接受其他的关键字参数的话，这两个方法就要同时提供，并且都要提供对应的参数签名。
	默认的 __prepare__() 方法接受任意的关键字参数，但是会忽略它们，
	所以只有当这些额外的参数可能会影响到类命名空间的创建时你才需要去定义 __prepare__() 方法。

	'''
	def __prepare__(cls, name, bases,*,debug = False,synchronize=False):
		pass
		return super().__prepare__(name,bases)
	
	def __new__(cls,name,bases,ns,*,debug=False,synchronize=False):
		pass
		return super().__new__(cls,name,bases,ns)

	def __init__(self,name,bases,ns,*,debug=False,synchronize=False):
		pass
		super().__init__(name,bases,ns)


class Spam(metaclass=MyMeta):
	debug = True
	synchronize = True
	pass






if __name__=="__main__":
	try:
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




