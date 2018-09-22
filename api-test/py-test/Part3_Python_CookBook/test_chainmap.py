#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/19'
Info:
        
"""

import os,traceback
from collections import ChainMap


def search_from_chain():
	a={'x':'get x from a','z':'get z from a'}
	b={'y':'get y from b','z':'get z from b'}
	c = ChainMap(a,b)
	
	# 按序先从a 查找，然后从b 查找
	print(c['x']) # get x from a
	print(c['y']) # get y from b
	print(c['z']) # get z from a
	
	print(len(c)) # 3
	print(list(c.keys())) # ['y', 'x', 'z']
	print(list(c.values())) # ['get y from b', 'get x from a', 'get z from a']
	
	c['z'] = 10 # 第一个dict 如果存在就修改第一个，否则就插入第一个
	c['w'] = 40

	print(c)
	del c['x']
	del c['y'] # 第一个如果不存在y,则报错
	print(c)


def test_child():
	values = ChainMap()
	values['x'] = 1
	
	values = values.new_child()
	values['x'] = 2
	
	values = values.new_child()
	values['x'] = 3
	
	print(values) # ChainMap({'x': 3}, {'x': 2}, {'x': 1})
	
	print(values['x']) # 3
	
	values = values.parents
	print(values['x']) # 2
	
	values = values.parents
	print(values['x']) # 1

def do_merge():
	'''
	覆盖更新
	:return:
	'''
	a={'x':1,'z':3}
	b={'y':2,'z':4}
	merged = dict(a)
	merged.update(b)
	print(merged) # {'x': 1, 'z': 4, 'y': 2}

def test_update():
	'''
	ChainMap 底层并不创建新dick，数据仍存储在原有数据结构中，ChainMap 只提供轮询访问机制
	:return:
	'''
	
	a = {'x': 1, 'z': 3 }
	b = {'y': 2, 'z': 4 }
	merged = ChainMap(a, b)
	print(merged['x']) # 1
	
	a['x'] = 42
	print(merged['x']) # 42
	
	



if __name__=="__main__":
	try:
		# search_from_chain()
		
		# test_child()
		
		# do_merge()
		
		test_update()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


