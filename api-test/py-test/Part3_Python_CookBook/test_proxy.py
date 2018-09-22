#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

class A:
	def samm(self,x):
		pass
	def foo(self):
		pass

class B1:
	def __init__(self):
		self._a = A()
	
	def spam(self,x):
		return self._a.spam(x)
	

	def foo(self):
		return self._a.foo()

	def bar(self):
		pass

class B2:
	def __init__(self):
		self._a = A()
	
	def bar(self):
		pass
	
	def __getattr__(self, name):
		'''
		自身属性不存在时，从被代理对象获取
		:param name:
		:return:
		'''
		return getattr(self._a,name)

class Proxy:
	def __init__(self,obj):
		self._obj = obj
		
	def __getattr__(self, name): # 此处的 attr 既指属性，又指方法，只有当代理对象 Proxy 中不存在的属性或方法，才会调用此处到被代理对象_obj 中查找
		print('getattr: ',self._obj,name)
		return getattr(self._obj,name)
	
	def __setattr__(self, key, value):
		if key.startswith('_'):
			super().__setattr__(key,value) # 给代理对象自己赋值
		else:
			print('setattr: {} -> {}'.format(key,value))
			setattr(self._obj,key,value) # 给被代理对象 _obj 赋值
		
	def delattr(self,name):
		if name.startswith('_'):
			super().__delattr__(name) # 删除自身属性
		else:
			print('delattr: {}'.format(name))
			delattr(self._obj,name) # 删除被代理对象_obj属性

# 通过继承关系，实现类似代理功能
class AA:
	def spam(self,x):
		print('A spam',x)
	def foo(self):
		print('A.foo')

class BB(AA):
	def spam(self,x):
		'''
		同时存在，先后被调用
		:param x:
		:return:
		'''
		print('B.spam')
		super().spam(x)
	
	def bar(self):
		'''
		只有子类存在
		:return:
		'''
		print('B.bar')

def test_hierachy():
	b = BB()
	b.spam(4)
	b.bar()
	b.foo() # 只有父类存在
	
# 通代理，实现功能整合
class AA1:
	def spam(self,x):
		print('A spam',x)
	def foo(self):
		print('A.foo')
	
class BB1:
	def __init__(self):
		self._a = AA1()
		
	def spam(self,x):
		print('B spam',x)
		self._a.spam(x)
		
	def bar(self):
		print('B.bar')
	
	def __getattr__(self, name):
		'''
		自身补存在的属性，通过__getattr__ 到被代理对象中去找
		:param name:
		:return:
		'''
		return getattr(self._a,name)


def test_hierachy2():
	b = BB1()
	b.spam(4)
	b.bar()
	b.foo() # 只有父类存在

class ListLike:
	def __init__(self):
		self._items = []
	
	def __getattr__(self, item):
		return getattr(self._items,item)
	
	def __str__(self):
		return '{}({})'.format(self.__class__.__name__,', '.join(str(x) for x in self._items))

def test_like():
	'''
	ListLike 内部关联了 list 类型属性，通过__getattr__ 可以拿到 list 内非 下划线开头的属性 和 方法，但不能调用下划线开头的 __len__
	已经基于 __getitem__ , __setitem__ , __delitem__ 的索引运算
	:return:
	'''
	a = ListLike()
	a.append(2)
	a.insert(0,1)
	print(a) # ListLike(1, 2)
	print(len(a)) # TypeError: object of type 'ListLike' has no len()

class ListLike2:
	def __init__(self):
		self._items = []
	
	def __getattr__(self, item):
		return getattr(self._items,item)
	
	def __str__(self):
		return '{}({})'.format(self.__class__.__name__,', '.join(str(x) for x in self._items))
	
	# 手动添加__len__ __getitem__ __setitem__ __delitem__ 使ListLike 像 List 一样工作
	def __len__(self):
		return len(self._items)
	
	def __getitem__(self, index):
		return self._items[index]
	
	def __setitem__(self, index, value):
		self._items[index] = value
	
	def __delitem__(self,index):
		del self._items[index]

def test_like2():
	ll = ListLike2()
	ll.append(1)
	ll.insert(0,0)
	ll[1]=2
	ll.remove(0)
	print(ll,ll[0],len(ll)) # ListLike2(2) 2 1




class Spam:
	def __init__(self,x):
		self.x = x
	
	def bar(self,y):
		print('Spam.bar',self.x,y)


def test_proxy():
	s = Spam(2)
	p = Proxy(s)
	print(p.x)
	p.x = 12
	p.bar(3)



if __name__=="__main__":
	try:
		# test_proxy()
		# test_hierachy()
		# test_hierachy2()
		# test_like()
		test_like2()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




