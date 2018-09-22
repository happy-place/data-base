#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback,json
from collections import OrderedDict
from itertools import zip_longest
    



'''
 OrderedDict 维持的是数据插入的顺序，底层通过双向链表实现，对插入顺序的维护。插入删除性能开销 和 存储开销比普通 dict 大很多
'''


def test_orderedDict():
	d = OrderedDict()
	d['foo'] = 5
	d['bar'] = 2
	d['spam'] = 3
	d['grok'] = 4
	
	for k in d:
		print(k,d[k])
	'''
	foo 5
	bar 2
	spam 3
	grok 4
	'''

def mk_orderedJson():
	d = OrderedDict()
	d['foo'] = 5
	d['bar'] = 2
	d['spam'] = 3
	d['grok'] = 4
	j = json.dumps(d)
	print(j) # {"foo": 5, "bar": 2, "spam": 3, "grok": 4}


def test_zip():
	prices = {'ACME': 45.23,'AAPL': 612.78, 'IBM': 205.55,'HPQ': 37.20,'FB': 10.75}
	
	# 通过kv 反转，利用 dict 天然对key进行排序功能，取最值
	min_price = min(zip(prices.values(),prices.keys()))
	max_price = max(zip(prices.values(),prices.keys()))
	
	print(min_price,max_price) # (10.75, 'FB') (612.78, 'AAPL')
	
	# zip 函数创建的是一个只能一次性访问的迭代器，重复使用会报错
	prices_sorted = sorted(zip(prices.values(),prices.keys()))
	print(prices_sorted) # [(10.75, 'FB'), (37.2, 'HPQ'), (45.23, 'ACME'), (205.55, 'IBM'), (612.78, 'AAPL')]
	
	prices_iterator = zip(prices.values(),prices.keys())
	print(min(prices_iterator))
	# print(max(prices_iterator)) # ValueError: max() arg is an empty sequence 迭代器只能使用一次
	
	# 对字典执行普通运算仅作用于键
	print(min(prices),max(prices)) # AAPL IBM
	print(min(prices.values()),max(prices.values())) # 专门去值进行运算 10.75 612.78
	
	min_val = prices[min(prices,key=lambda k:prices[k])] # 对prices 从 value 维度取最小值对应的 k： min(prices,key=lambda k:prices[k])
	print(min_val) # 10.75
	
	# 最大最小值相等时，min max 取出的实体存在差异
	prices = {'AAA':12.3,"BBB":12.3}
	print(min(zip(prices.values(),prices.keys()))) # (12.3, 'AAA')
	print(max(zip(prices.values(),prices.keys()))) # (12.3, 'BBB')
	
	# 查找相同key 或 value
	a = {'x':1,'y':2,'z':3}
	b = {'w':10,'x':11,'y':2}
	
	print(a.keys() & b.keys()) # 集合进行 & 操作取交集 {'x', 'y'}
	print(a.keys() - b.keys()) # 集合差集 {'z'}
	print(a.items() & b.items()) # kv 集合交集 {('y', 2)}
	
	# 局部过滤 字典a 中删除 key 为z,w 的kv 构建新dict
	c = {key:a[key] for key in a.keys() - {'z','w'}}
	print(c) # {'y': 2, 'x': 1}


def test_plain():
	xpts = [1, 5, 4, 2, 10, 7]
	ypts = [101, 78, 37, 15, 62, 99,100]
	
	for x,y in zip(xpts,ypts):
		print(x,y)
		# zip 长度取决于最短集合长度
		'''
		1 101
		5 78
		4 37
		2 15
		10 62
		7 99
		'''

def test_zip_longest():
	xpts = [1, 5, 4, 2, 10, 7]
	ypts = [101, 78, 37, 15, 62, 99,100]
	
	# 最长拉链，默认使用None填空
	for x,y in zip_longest(xpts,ypts):
		print(x,y)
		'''
		1 101
		5 78
		4 37
		2 15
		10 62
		7 99
		None 100
		'''
	
	for x,y in zip_longest(xpts,ypts,fillvalue=0):
		print(x,y)
		'''
		1 101
		5 78
		4 37
		2 15
		10 62
		7 99
		0 100
		'''
	
def mk_dict():
	headers = ['name', 'shares', 'price']
	values = ['ACME', 100, 490.1]
	a = dict(zip(headers,values))
	
	for name,val in a.items():
		print(name,'=',val)
		'''
		name = ACME
		shares = 100
		price = 490.1
		'''
	
	for name,val in zip(headers,values):
		print(name,'=',val)
		'''
		name = ACME
		shares = 100
		price = 490.1
		'''
	
	a = [1,2,3]
	b = [10,11,12]
	c = ['x','y','z']
	
	for x,y,z in zip(a,b,c):
		print(x,y,z)
		'''
		1 10 x
		2 11 y
		3 12 z
		'''

def save_2_list():
	a = [1,2,3]
	b = [10,11,12]
	c = zip(a,b) # 使用zip 创建的是迭代器，用list 包装可以保持内容
	print(type(c)) # <class 'zip'>
	
	print(list(c)) # [(1, 10), (2, 11), (3, 12)]


if __name__=="__main__":
	try:
		# test_plain()
		# test_zip_longest()
		# mk_dict()
		save_2_list()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)