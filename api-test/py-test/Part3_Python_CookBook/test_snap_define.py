#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from collections import OrderedDict

class Typed:
	_expected_type = type(None)
	def __init__(self,name = None):
		self._name = name
	
	def __set__(self, instance, value):
		if not isinstance(value,self._expected_type):
			raise TypeError('Expected '+str(self._expected_type))
		instance.__dict__[self._name] = value
		
class Integer(Typed):
	_expected_type = int
	
class Float(Typed):
	_expected_type = float
	
class String(Typed):
	_expected_type = str

class OrderedMeta(type):
	def __new__(cls, clsname,bases,clsdict):
		d = dict(clsdict)
		order = []
		for name,value in clsdict.items():
			if isinstance(value,Typed):
				value._name = name
				order.append(name)
		d['_order'] = order
		return type.__new__(cls,clsname,bases,d)
	
	@classmethod
	def __prepare__(metacls, name, bases):
		return OrderedDict()

class Srtructure(metaclass=OrderedMeta):
	def as_csv(self):
		return ','.join(str(getattr(self,name)) for name in self._order)

class Stock(Srtructure):
	name = String()
	shares = Integer()
	price = Float()
	
	def __init__(self,name,price,shares):
		self.name = name
		self.price = price
		self.shares = shares


def test_stock():
	s = Stock('aa',12.3,12)
	print(s.as_csv()) # 实例化顺序与入参顺序无关 aa,12,12.3
	
'''
OrderedDict 维护了子类的属性列表
'''
class NoDupOrderedDict(OrderedDict):
	def __init__(self,clsname):
		self.clsname = clsname
		super().__init__()
	def __setitem__(self, key, value):
		if key in self: # 重复定义函数报错TypeError: spam already defined in AA
			raise TypeError('{} already defined in {}'.format(key,self.clsname))
		super().__setitem__(key,value)

class OrderedMeta1(type):
	def __new__(cls,clsname,bases,clsdict):
		d = dict(clsdict)
		d['_order'] = [name for name in clsdict if name[0] !='_']
		return type.__new__(cls,clsname,bases,d)
	
	@classmethod
	def __prepare__(metacls, clsname, bases):
		return NoDupOrderedDict(clsname)

class AA(metaclass=OrderedMeta1):
	def spam(self):
		pass
	
	def spam(self):
		pass


if __name__=="__main__":
	try:
		# test_stock()
		a =AA()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




