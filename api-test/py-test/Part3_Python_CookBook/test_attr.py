#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,math

class Person:
	def __init__(self,first_name):
		self.first_name  = first_name
	
	@property
	def first_name(self):
		return self._first_name
	
	@first_name.setter
	def first_name(self,value):
		if not isinstance(value,str):
			raise TypeError('Excepted str')
		self._first_name = value
	
	@first_name.deleter
	def first_name(self):
		raise AttributeError("Can't delete attribute")


def test_class():
	p = Person('tom') # __init__
	print(p.first_name) # 	@property getter
	p.first_name = 'jack' # @first_name.setter
	print(p.first_name)
	del p.first_name # 调用到 @first_name.deleter
	
		
class Monkey:
	def __init__(self,first_name):
		self.set_first_name(first_name)

	def get_first_name(self):
		return self._first_name
	
	def set_first_name(self,value):
		if not isinstance(value,str):
			raise TypeError('Excepted str')
		self._first_name = value
	
	def del_first_name(self):
		raise AttributeError("Can't delete attribute")
	
	name = property(get_first_name,set_first_name,del_first_name)
	# 通过property 将get_first_name,set_first_name,del_first_name 这三个动作绑定到name 上
	
		
def test_class2():
	print(Monkey.name.fget)
	print(Monkey.name.fset)
	print(Monkey.name.fdel)
	
	m = Monkey('kk')
	print(m.name)
	m.name = 'yy'
	print(m.name)
	del m.name
	
class Circle:
	def __init__(self,radius):
		self.radius = radius
	
	@property
	def area(self):
		return math.pi * self.radius**2
	
	@property
	def diameter(self):
		return self.radius * 2
	
	@property # 将函
	def perimeter(self):
		return 2 * math.pi * self.radius


def test_property():
	c = Circle(1)
	print(c.radius,c.area,c.diameter,c.perimeter) # 1 3.141592653589793 2 6.283185307179586

if __name__=="__main__":
	try:
		# test_class()
		# test_class2()
		test_property()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




