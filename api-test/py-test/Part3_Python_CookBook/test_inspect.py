#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,inspect,logging
from inspect import Signature,Parameter,signature



def test_sig():
	'''
	手动创建如下函数的方法签名
	def func(x,y=42,*,z=None):
	pass
	:return:
	'''
	parms = [Parameter('x',Parameter.POSITIONAL_OR_KEYWORD), # x 既能以位置参数形式出现，又能以关键参数形式出现
	         Parameter('y',Parameter.POSITIONAL_OR_KEYWORD,default=42), # y 既能以位置参数形式出现，又能以关键参数形式出现,默认值为 42
	         Parameter('z',Parameter.KEYWORD_ONLY,default=None) # z 只能以关键参数形式出现,默认值为 None
	         ]
	sig = Signature(parms)
	print(sig) # (x, y=42, *, z=None)
	
	def func(*args,**kwargs):
		bound_values = sig.bind(*args,**kwargs)
		for name,value in bound_values.arguments.items():
			print(name,value)
	
	
	func(1,2,z=3)
	'''
	x 1
	y 2
	z 3
	'''
	
	func(1)
	'''
	x 1
	'''
	func(y=2,x=1)
	'''
	x 1
	y 2
	'''
	
	# func(1,2,3,4) # TypeError: too many positional arguments 多传 报错
 

def make_sig(*names):
	# 参数既可是位置参数又可是关键参数
	parms = [Parameter(name,Parameter.POSITIONAL_OR_KEYWORD) for name in names]
	return Signature(parms)
	
class Sturcture:
	__signature__ = make_sig()
	def __init__(self,*args,**kwargs):
		bound_values = self.__signature__.bind(*args,**kwargs)
		for name,value in bound_values.arguments.items():
			setattr(self,name,value)

class Stock(Sturcture):
	__signature__ = make_sig('name','shares','price')

class Point(Sturcture):
	__signature__ = make_sig('x','y')

def test_inspect():
	print(inspect.signature(Stock)) # (name, shares, price)
	s1 = Stock('aa',100,12.3)
	s2 = Stock('aa',100,12.3)


class StructureMeta(type):
	def __new__(cls, clsname,bases,clsdict):
		clsdict['__signature__'] = make_sig(*clsdict.get('_fields',[]))
		return super().__new__(cls,clsname,bases,clsdict)
	
class Structure1(metaclass=StructureMeta):
	_fields = []
	def __init__(self,*args,**kwargs):
		bound_values = self.__signatrue__.bind(*args,**kwargs)
		for name,value in bound_values.arguments.items():
			setattr(self,name,value)

class Stock(Structure1):
	_fields = ['name','shares','price']
	
class Point(Structure1):
	_fields = ['x','y']


def test_inspect2():
	print(inspect.signature(Stock)) # (name, shares, price)
	print(inspect.signature(Point)) # (x, y)


# 从元类控制 方法名必须全部小写，不能大小写混杂
class NoMixedCaseMeta(type):
	def __new__(cls, clsname,bases,clsdict):
		for name in clsdict:
			if name.lower() != name:
				raise TypeError('Bad attribute name: '+name)
		return super().__new__(cls,clsname,bases,clsdict)

class Root(metaclass=NoMixedCaseMeta):
	pass

class A(Root):
	def foo_bar(self):
		pass

# 大小写混杂，编译不通过
# class B(Root):
# 	def fooBar(self):
# 		pass


def ab():
	a = A()
	# b = B()

class MatchSignaturesMeta(type):
	
	def __init__(self, clsname, bases, clsdict):
		super().__init__(clsname, bases, clsdict)
		sup = super(self, self)
		for name, value in clsdict.items():
			if name.startswith('_') or not callable(value):
				continue
			# Get the previous definition (if any) and compare the signatures
			prev_dfn = getattr(sup,name,None)
			if prev_dfn:
				prev_sig = signature(prev_dfn)
				val_sig = signature(value)
				if prev_sig != val_sig:
					logging.warning('Signature mismatch in %s. %s != %s',
					                value.__qualname__, prev_sig, val_sig)
					
class Root1(metaclass=MatchSignaturesMeta):
	pass

class A1(Root1):
	def foo(self,x,y):
		pass
	
	def spam(self,x,*,z):
		pass

class B1(A1):
	# def foo(self,a,b):
	# 	pass
	# def spam(self,x,y):
	# 	pass
	#
	def foo(self,x,y):
		pass
	
	def spam(self,x,*,z):
		pass

def test_metachk():
	a1 = A1()
	b1 = B1()




if __name__=="__main__":
	try:
		# test_sig()
		# test_inspect()
		# test_inspect2()
		# ab()
		test_metachk()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




