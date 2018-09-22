#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,math

'''
通过继承方式，使用结构体管理对象属性，而无需创建繁多的 __init__() 函数
'''
class Structure1:
	_fields = []
	
	def __init__(self,*args):
		if len(args) != len(self._fields):
			raise TypeError('Excepted {} args'.format(self._fields))
		for name,value in zip(self._fields,args):
			setattr(self,name,value)

	def __str__(self):
		return '{clsname}({kv})'.format(clsname=self.__class__.__name__, kv=str([k+" = "+str(v) for k,v in self.__dict__.items()])[1:-1])
	
	
class Stock(Structure1):
	_fields = ['name','shares','price']

class Point(Structure1):
	_fields = ['x','y']

class Circle(Structure1):
	_fields = ['radius']

	def area(self):
		return math.pi * self.radius ** 2

def test_fast_init():
	s = Stock('ABCD',50,12.3)
	print(s,s.name) # Stock('name = ABCD', 'shares = 50', 'price = 12.3')  ABCD

	p = Point(2,3)
	print(p)
	
	c = Circle(4)
	print(c)
	
	s2 = Stock('ABCD',50)
	

class Structure2:
	_fields = []
	
	def __init__(self,*args,**kwargs):
		if len(args) > len(self._fields):
			raise TypeError('Excepted {} args'.format(len(self._fields)))
		
		for name,value in zip(self._fields,args):
			setattr(self,name,value) # 优先通过位置参数定义
		
		for name in self._fields[len(args):]:
			setattr(self,name,kwargs.pop(name)) # 匹配不上的，通过关键参数定义k=v, 不再_fields集合内的额外属性还能继续被添加
		
		if kwargs:
			raise TypeError('Invalid args: {}'.format('.'.join(kwargs)))
	
	def __str__(self):
		return '{clsname}({kv})'.format(clsname=self.__class__.__name__, kv=str([k+" = "+str(v) for k,v in self.__dict__.items()])[1:-1])


class Stock2(Structure2):
	_fields = ['name','shares','price']
	
	
def test_fast_init2():
	s1 = Stock2('ABCD',shares=50,price = 12.3)
	print(s1)


class Structure3:
	_fields = []
	
	def __init__(self,*args,**kwargs):
		if len(args) != len(self._fields):
			raise TypeError('Excepted {} args'.format(len(self._fields)))
		
		for name,value in zip(self._fields,args): # _fields 中已经存在的属性通过 args 定义
			setattr(self,name,value)
		
		extra_args = kwargs.keys() - self._fields # 不再 _fields 中的属性通过 kwargs 定义
		
		for name in extra_args:
			setattr(self,name,kwargs.pop(name))
		
		if kwargs: # args ,kwargs 中存在交叉定义时，报错
			raise TypeError('Duplicate values for {}'.format('.'.join(kwargs)))
	
	def __str__(self):
		return '{clsname}({kv})'.format(clsname=self.__class__.__name__, kv=str([k+" = "+str(v) for k,v in self.__dict__.items()])[1:-1])


class Stock3(Structure3):
	_fields = ['name','shares','price']


def test_fast_init3():
	s1 = Stock3('ABCD',50,12.3, age=20)
	print(s1) # Stock3('name = ABCD', 'shares = 50', 'price = 12.3', 'age = 20')


class Stock4:
	__slots__ = ['name','shares','price']
	
	def __init__(self,*args):
		self.name = args[0]
		self.shares = args[1]
		self.price = args[2]
	
	def __str__(self):
		return 'Stock4("name"={},"shares"={},"price"={})'.format(self.name,self.shares,self.price)



class Stock5:
	_fields = ['name','shares','price']
	
	def __init__(self,*args):
		if len(args) != len(self._fields):
			raise TypeError('Excepted {} args'.format(len(self._fields)))
		
		self.__dict__.update(zip(self._fields,args))
	
	def __str__(self):
		return '{clsname}({kv})'.format(clsname=self.__class__.__name__, kv=str([k+" = "+str(v) for k,v in self.__dict__.items()])[1:-1])




def test_slots():
	s1 = Stock4('tom',10,12.3)
	# s1.age = 12  __slots 不能继续添加属性了
	print(s1) # Stock4("name"=tom,"shares"=10,"price"=12.3)
	s2 = Stock5('tom',10,12.3) # dict 还可以继续添加
	s2.age = 12
	print(s2) # Stock5('name = tom', 'shares = 10', 'price = 12.3', 'age = 12')




if __name__=="__main__":
	try:
		
		# test_fast_init()
		# test_fast_init2()
		# test_fast_init3()
		test_slots()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




