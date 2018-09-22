#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,io,collections
from abc import ABCMeta,abstractmethod

class IStream(metaclass=ABCMeta):
	@abstractmethod
	def read(self,maxbytes = -1):
		pass
	
	@abstractmethod
	def write(self,data):
		pass


class SocketStream(IStream):
	'''
	以继承方式，遵循接口规约
	'''
	def read(self,maxbytes=-1):
		pass
	
	def write(self,data):
		pass

def serialize(stream):
	if not isinstance(stream,IStream): # 接口用来约定具备某些功能的样板
		raise TypeError('Excepted an IStream')
	pass

def test_interface():
	# a = IStream() # TypeError: Can't instantiate abstract class IStream with abstract methods read, write
	st = SocketStream()
	serialize(st)
	
	'''
	以注册方式遵循接口规约
	'''
	IStream.register(io.IOBase)
	
	with open('num1.txt','r') as f:
		print(isinstance(f,IStream)) # True
	
	
class A(metaclass=ABCMeta):
	'''
	@abstractmethod 可同时注解静态方法，类方法，属性
	'''
	@property
	@abstractmethod
	def name(self):
		pass

	@name.setter
	@abstractmethod
	def name(self,value):
		pass

	@classmethod
	@abstractmethod
	def method1(cls): # 类方法有静态方法区别在于类方法不需要cls,类方法需要cls
		pass
	
	@staticmethod
	@abstractmethod
	def method1():
		pass


def test_collections():
	x = 'abc'
	print(isinstance(x,collections.Sequence))
	
	x = [1,2,3]
	print(isinstance(x,collections.Iterable))
	
	x = 'abc'
	print(isinstance(x,collections.Sized))
	
	x = {'name':'tom','age':12}
	print(isinstance(x,collections.Mapping))





if __name__=="__main__":
	try:
		# test_interface()
		test_collections()
		
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




