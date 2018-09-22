#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,collections
import bisect

class SortedItems(collections.Sequence):
	'''
	继承方式创建排Seq类型
	'''
	def __init__(self,initial = None):
		self._items = sorted(initial) if initial is not None else []
	
	def __getitem__(self, index):
		return self._items[index] # 索引取值
	
	def __len__(self):
		return len(self._items) # 获取长度
	
	def add(self,item):
		bisect.insort(self._items,item) # 二分插入
	
	def __str__(self):
		return '{}({})'.format(self.__class__.__name__, ', '.join(str(x) for x in self._items))


def test_sortedItems():
	si = SortedItems({3,2,1,4})
	print(si) # SortedItems(1, 2, 3, 4)
	print(si[0],si[2]) # 1 3
	si.add(2)
	print(si,si.__len__()) # SortedItems(1, 2, 2, 3, 4) 5

	print(isinstance(si,collections.Sequence))
	print(isinstance(si,collections.Sized))
	print(isinstance(si,collections.Iterable))
	print(isinstance(si,collections.Container))
	print(isinstance(si,collections.Mapping)) # False
	
	
class Items(collections.MutableSequence):
	def __init__(self,initial=None):
		self._items = list(initial) if initial is not None else []
	
	def __getitem__(self,index):
		print('Getting: {}'.format(index))
		return self._items[index]
	
	def __setitem__(self, index, value):
		print('Setting {} -> {}'.format(index,value))
		self._items[index] = value
	
	def __delitem__(self,index):
		print('Deleting {}'.format(index))
	
	def insert(self,index,value):
		print('Inserting: {}'.format(index))
		self._items.insert(index,value)
	
	def __len__(self):
		print('len')
		return len(self._items)

def test_mutualableSeq():
	a = Items([1,2,3])
	print(len(a))
	a.append(4)
	a.append(5)
	print(a.count(3))
	a.remove(3)
	print(a)


if __name__=="__main__":
	try:
		# test_sortedItems()
		test_mutualableSeq()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




