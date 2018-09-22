#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from collections import defaultdict
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn


class LoggedMappingMixin:
	__slots__ = ()
	
	def __getitem__(self, key):
		print('Getting ',str(key))
		return super().__getitem__(key)
	
	def __setitem__(self,key,value):
		print('Setting {} = {!r}'.format(key,value))
		return super().__setitem__(key,value)
	
	def __delitem__(self,key):
		print('Deleting ',str(key))
		return super().__delitem__(key)

class SetOnceMappingMixin:
	'''
	运行对混入集合类型通过 append 添加新元素，但不允许直接基于 index 修改元素
	'''
	__slots__ = ()
	
	def __setitem__(self, key, value):
		# print(self)
		if key in self:
			raise KeyError(str(key) + ' already set')
		return super().__setitem__(key,value)

class StringKeyMappingMixin:
	__slots__ = ()
	
	def __setitem__(self, key, value):
		if key in self:
			raise KeyError('keys must be strings')
		return super().__setitem__(key,value)

class LoggedDict(LoggedMappingMixin,dict):
	'''
	LoggedMappingMixin 用于对 dict 进行扩展，单独 LoggedDict 根本无法使用
	'''
	pass

class SetOnceDefaultDict(SetOnceMappingMixin,defaultdict):
	pass


def test_mixin1():
	d = LoggedDict()
	d['x'] = 23 # Setting x = 23
	print(d['x'])
	# Getting  x
	# 23
	del d['x'] # Deleting  x

def test_mixin2():
	sd = SetOnceDefaultDict(list)
	sd['x'].append(2)
	print(sd)
	sd['x'].append(3)
	sd['x'].append(4)
	print(sd)
	sd['x'] = 23 # KeyError: 'x already set'
	
class ThreadedXMLRPCServer(ThreadingMixIn,SimpleXMLRPCServer):
	'''
	将ThreadingMixIn,SimpleXMLRPCServer 动态混入到一起，是的RPC服务具备多线程功能
	'''
	pass

def LoggedMapping(cls):
	'''
	类装饰器
	'''
	# 获取被装饰类型 LoggedDict dict 的函数
	cls_getitem = cls.__getitem__
	cls_setitem = cls.__setitem__
	cls_delitem = cls.__delitem__
	
	# 基于 对被装饰类的函数进行封装改造
	def __getitem__(self,key):
		print('Getting ',str(key))
		return cls_getitem(self,key)
	
	def __setitem__(self,key,value):
		print('Setting {} = {!r}'.format(key,value))
		return cls_setitem(self,key,value)
	
	def __delitem__(self,key):
		print('Deletint ',str(key))
		return cls_delitem(self,key)
	
	# 将改造后的函数，替换掉被装饰类的函数
	cls.__getitem__ = __getitem__
	cls.__setitem__ = __setitem__
	cls.__delitem__ = __delitem__
	
	# 返回函数被替换的被装饰类的类型
	return cls

@LoggedMapping
class LoggedDict(dict):
	pass
	
def test_cls_mixin():
	ld = LoggedDict()
	ld.update({'a':'A'})
	print(ld['a'])
	

if __name__=="__main__":
	try:
		# test_mixin1()
		# test_mixin2()
		test_cls_mixin()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




