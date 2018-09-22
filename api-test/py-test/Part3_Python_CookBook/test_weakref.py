#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,weakref,gc

class Node:
	def __init__(self,value):
		self.value = value
		self._parent = None
		self.children = []
	
	def __repr__(self):
		return 'Node({!r:})'.format(self.value)
	
	@property
	def parent(self):
		return None if self._parent is None else self._parent()
	
	@parent.setter # 设置 parent时，设置的都是弱引用
	def parent(self,node):
		self._parent = weakref.ref(node) # parent 节点消失，子节点对 parent的引用也会自主消失
	
	def add_child(self,child):
		self.children.append(child)
		child.parent = self # 通过@parent.setter 注解的def parent(self,node):方法实现针对 parent 的引用，一旦 parent 消失，自动返回 None


def test_node():
	root = Node('parent')
	c1 = Node('child')
	root.add_child(c1)
	print(c1.parent) # Node('parent')
	del root
	print(c1.parent) # None

class Data:
	def __del__(self):
		print('Data.__del__')

class DataNode:
	def __init__(self):
		self.data = Data()
		self.parent = None
		self.children = []
	
	def add_child(self,child):
		self.children.append(child)
		child.parent = self

def test_del():
	# 可以正常删除
	a = Data()
	del a  # test_del
	a = DataNode()
	del a # Data.__del__
	
	# 父子之间的循环引用永远存在，删除彼此失效，出现内存泄漏
	# b = DataNode()
	# b.add_child(DataNode())
	# del b
	
	# gc.collect() # 即便使用 gc 进行强制垃圾回收有无用


def test_weakref():
	a = DataNode()
	'''
	通过弱引用访问对象不会引起引用计数指针增加
	'''
	a_ref = weakref.ref(a)
	print(a_ref,a_ref()) # <weakref at 0x110728d18; to 'DataNode' at 0x1107561d0> <__main__.DataNode object at 0x102574da0>
	del a # Data.__del__
	print(a_ref,a_ref()) # <weakref at 0x110728d18; dead>  None



if __name__=="__main__":
	try:
		# test_node()
		# test_del()
		
		test_weakref()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




