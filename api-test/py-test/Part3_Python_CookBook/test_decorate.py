#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

# 对创建对象进行类型检查
# 约束基类
class Desriptor:
	def __init__(self,name=None,**opts):
		self.name = name
		for key,value in opts.items():
			setattr(self,key,value)
		
	def __set__(self, instance, value):
		instance.__dict__[self.name] = value

class Typed(Desriptor):
	excepted_type = type(None)
	
	def __set__(self, instance, value):
		if not isinstance(value,self.excepted_type):
			raise TypeError('Excepted {}'.format(str(self.excepted_type)))
		super().__set__(instance,value)

class Unsigned(Desriptor):
	def __set__(self, instance, value):
		if value < 0 :
			raise ValueError('Excepted >= 0')
		super().__set__(instance,value)

class MaxSized(Desriptor):
	def __init__(self,name=None,**opts):
		if 'size' not in opts:
			raise TypeError('missing size option')
		super().__init__(name,**opts)
		
	def __set__(self, instance, value):
		if len(value) >= self.size:
			raise ValueError('size must be < {}'.format(str(self.size)))
		super().__set__(instance,value)

# 基础类型
class Integer(Typed):
	excepted_type = int

class UnsignedInteger(Integer,Unsigned):
	pass

class Float(Typed):
	excepted_type = float

class UnsignedFloat(Float,Unsigned):
	pass

class String(Typed):
	excepted_type = str

class SizedString(String,MaxSized):
	pass

# 自定义类型
class Stock:
	name = SizedString('name',size=8)
	shares = UnsignedInteger('shares')
	price = UnsignedFloat('price')
	
	def __init__(self,name,shares,price):
		self.name = name
		self.shares = shares
		self.price = price
		
	def __str__(self):
		return '{}({})'.format(self.__class__.__name__,', '.join('{}={}'.format(str(k),v) for k,v in self.__dict__.items()))


def test_stock():
	s = Stock('tom',12,12.3) # Stock(name=tom, shares=12, price=12.3)
	print(s)
	s.shares = 1.2 # TypeError: Excepted <class 'int'> 类型约束生效了
	print(s)
	
	
# 方案2：通过装饰器约束类型
def check_attributes(**kwargs):
	def decorate(cls):
		for key,value in kwargs.items():
			if isinstance(value,Desriptor):
				value.name = key
				setattr(cls,key,value)
			else:
				setattr(cls,key,value(key))
		return cls
	return decorate


@check_attributes(name=SizedString(size = 8),shares = UnsignedInteger,price=UnsignedFloat)
class Stock2:
	def __init__(self,name,shares,price):
		self.name = name
		self.shares = shares
		self.price = price
	
	def __str__(self):
		return '{}({})'.format(self.__class__.__name__,', '.join('{}={}'.format(str(k),v) for k,v in self.__dict__.items()))


# 方案3：使用元类
class checkedmeta(type):
	def __new__(cls,clsname,bases,methods):
		for key,value in methods.items():
			if isinstance(value,Desriptor):
				value.name = key # 绑定装饰器名称
		return type.__new__(cls,clsname,bases,methods)


def test_stock2():
	s = Stock2('tom',12,12.3)
	print(s)
	s.shares = 1.2


class Stock3(metaclass=checkedmeta):
	name = SizedString(size = 8)
	shares = UnsignedInteger()
	price = UnsignedFloat()
	
	def __init__(self,name,shares,price):
		self.name = name
		self.shares = shares
		self.price = price
	
	def __str__(self):
		return '{}({})'.format(self.__class__.__name__,', '.join('{}={}'.format(str(k),v) for k,v in self.__dict__.items()))


def test_stock3():
	s = Stock3('tom',12,12.3) # Stock3(name=tom, shares=12, price=12.3)
	print(s)
	s.shares = 1.2


class Point:
	x = Integer('x')
	y = Integer('y')
	
class Point(metaclass=checkedmeta):
	x = Integer()
	y = Integer()

# Decorator for applying type checking
def Typed(expected_type, cls=None):
	if cls is None:
		return lambda cls: Typed(expected_type, cls)
	super_set = cls.__set__
	
	def __set__(self, instance, value):
		if not isinstance(value, expected_type):
			raise TypeError('expected ' + str(expected_type))
		super_set(self, instance, value)
	
	cls.__set__ = __set__
	return cls


# Decorator for unsigned values
def Unsigned(cls):
	super_set = cls.__set__
	
	def __set__(self, instance, value):
		if value < 0:
			raise ValueError('Expected >= 0')
		super_set(self, instance, value)
	
	cls.__set__ = __set__
	return cls


# Decorator for allowing sized values
def MaxSized(cls):
	super_init = cls.__init__
	
	def __init__(self, name=None, **opts):
		if 'size' not in opts:
			raise TypeError('missing size option')
		super_init(self, name, **opts)
	
	cls.__init__ = __init__
	
	super_set = cls.__set__
	
	def __set__(self, instance, value):
		if len(value) >= self.size:
			raise ValueError('size must be < ' + str(self.size))
		super_set(self, instance, value)
	
	cls.__set__ = __set__
	return cls


# Specialized descriptors
@Typed(int)
class Integer(Desriptor):
	pass


@Unsigned
class UnsignedInteger(Integer):
	pass


@Typed(float)
class Float(Desriptor):
	pass


@Unsigned
class UnsignedFloat(Float):
	pass


@Typed(str)
class String(Desriptor):
	pass


@MaxSized
class SizedString(String):
	pass








if __name__=="__main__":
	try:
		# test_stock2()
		test_stock3()
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




