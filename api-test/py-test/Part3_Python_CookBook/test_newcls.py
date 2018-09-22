#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,types,abc

def __init__(self,name,shares,price):
	self.name = name
	self.shares = shares
	self.price= price

def cost(self):
	return self.shares * self.price

cls_dict = {'__init__':__init__,'cost':cost}

# 无元类，无参数
def test_mkcls():
	# 变成方式创建类
	Stock = types.new_class('Stock', # 类名
	                        (), # *args 元信息
	                        {}, # **kwargs 定义信息
	                        lambda ns:ns.update(cls_dict) # 函数字典
	                        )
	Stock.__module__ = __name__
	
	s = Stock('ABC',100,12.3)
	print(s.price,s.cost())


# 有元类，无参数
def test_mkcls2():
	Stock1 = types.new_class('Stock1', # 类名
	                         (), # *args 元信息
	                         {'metaclass':abc.ABCMeta}, # **kwargs 定义信息
	                         lambda ns:ns.update(cls_dict) # 函数字典
	                         )
	Stock1.__module__ = __name__
	print(type(Stock1)) # <class 'abc.ABCMeta'>


class Base(debug=True,typecheck=False):
	def foo(self):
		pass

# 有元类，有参数
def test_mkcls3():
	Stock3 = types.new_class('Stock3',(Base,),{'debug':True},lambda ns:ns.update(cls_dict))
	Stock3.__module__ = __name__
	print(type(Stock3)) # <class 'abc.ABCMeta'>






if __name__=="__main__":
	try:
		# test_mkcls()
		# test_mkcls2()
		test_mkcls3()
		
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




