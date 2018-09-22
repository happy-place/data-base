#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

class Integer:
	'''
	类型描述器
	'''
	def __init__(self,name): # 属性名
		self.name = name
	
	def __get__(self,instance,cls):
		if instance is None:
			return self
		else:
			return instance.__dict__[self.name] # 获取属性
	
	def __set__(self, instance, value):
		if not isinstance(value,int):
			raise TypeError('Excepted an int')
		instance.__dict__[self.name] = value # 设置属性
	
	def __delete__(self, instance):
		del instance.__dict__[self.name] # 删除属性

class Point:
	'''
	描述器的一个比较困惑的地方是它只能在类级别被定义，而不能为每个实例单独定义
	'''
	x = Integer('x')
	y = Integer('y')
	
	def __init__(self,x,y):
		# self.x = Integer('x') 此处使用描述器会报错
		self.x = x
		self.y = y

def test_descrtptor():
	p = Point(1,2)
	print(p.x)
	
	p.x = 3
	print(p.x)
	
	# p.x = 2.3 # TypeError: Excepted an int
	# print(p.x)

# Descriptor for a type-checked attribute
class Typed:
	def __init__(self, name, expected_type):
		self.name = name
		self.expected_type = expected_type
		
	def __get__(self, instance, cls):
		if instance is None:
			return self
		else:
			return instance.__dict__[self.name]
	
	def __set__(self, instance, value):
		if not isinstance(value, self.expected_type):
			raise TypeError('Expected ' + str(self.expected_type))
		instance.__dict__[self.name] = value
		
	def __delete__(self, instance):
		del instance.__dict__[self.name]

# Class decorator that applies it to selected attributes
def typeassert(**kwargs):
	def decorate(cls):
		for name, expected_type in kwargs.items():
			# Attach a Typed descriptor to the class
			setattr(cls, name, Typed(name, expected_type))
		return cls
	return decorate

# Example use
@typeassert(name=str, shares=int, price=float)
class Stock:
	def __init__(self, name, shares, price):
		self.name = name
		self.shares = shares
		self.price = price
		
	def __str__(self):
		return 'Stock(name="{0}",shares={1},price={2})'.format(self.name,self.shares,self.price)



if __name__=="__main__":
	try:
		# test_descrtptor()
		
		s = Stock(name='tom',shares=1,price=1.2)
		print(s) # Stock(name="tom",shares=1,price=1.2)
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




