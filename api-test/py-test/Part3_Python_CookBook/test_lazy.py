#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,math

class lazyproperty:
	def __init__(self,func):
		self.func = func
	
	def __get__(self, instance, cls):
		if instance is None:
			return self
		else:
			value = self.func(instance)
			setattr(instance,self.func.__name__,value)
			return value
		
		
def lazypeoperty1(func):
	name = '_lazy_'+func.__name__
	@property
	def lazy(self):
		if hasattr(self,name):
			return getattr(self,name)
		else:
			value = func(self)
			setattr(self,name,value)
			return value
	return lazy


class Circle:
	def __init__(self,radius):
		self.radius = radius
	
	@lazyproperty
	def area(self):
		print('Computing area')
		return math.pi * self.radius ** 2
	
	@lazyproperty
	def perimeter(self):
		print('Computing perimeter')
		return 2*math.pi * self.radius

def test_lazy():
	c = Circle(3)
	
	print(vars(c))
	print(c.radius)
	'''
	{'radius': 3}
	3
	'''
	
	print(c.area)
	print(vars(c))
	'''
	Computing area
	28.274333882308138
	{'radius': 3, 'area': 28.274333882308138}
	'''

	print(c.perimeter)
	print(vars(c))
	''' 首次提取，需要计算
	Computing perimeter
	18.84955592153876
	{'radius': 3, 'area': 28.274333882308138, 'perimeter': 18.84955592153876}
	'''

	print(c.area)
	print(c.perimeter)
	''' 属性已经存在直接提取
	28.274333882308138
	18.84955592153876
	'''

	c.perimeter = 50 # {'radius': 3, 'area': 28.274333882308138, 'perimeter': 50} 运行被修改
	print(vars(c))
	print(c.perimeter)
	
	

if __name__=="__main__":
	try:
		test_lazy()
	
	
	
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




