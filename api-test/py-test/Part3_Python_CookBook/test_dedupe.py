#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback

def dedupe1(items):
	seen = list()
	for item in items:
		if item not in seen: # 如果对象不存在就在执行完 yield 下面的代码后，抛出此item（相当于return）
			yield item
			seen.append(item)

# 通过迭代器去重
def dedupe2(items,key=None):
	seen = set()
	for item in items:
		val = item if key is None else key(item) # 如果传入的是单元素，直接进行去重，否则解封然后去重
		if val not in seen:
			yield item
			seen.add(val)


if __name__=="__main__":
	try:
		# for + yield 返回的是生成器对象，需要包装到集合中，才能落地
		# print(dedupe(['a','b','a','c'])) # <generator object dedupe at 0x105ab9150>
		print(list(dedupe1(['a','b','a','c'])))
		
		print(list(dedupe2(['a','b','a','c']))) # ['a', 'b', 'c']
		
		a = [ {'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]
		print(list(dedupe2(a,key=lambda d:(d['x'],d['y'])))) # [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
		
		print(set(['a','b','a','c'])) # {'a', 'c', 'b'}
		
		# 读取文件消除重复行
		with open('test.txt','r') as f:
			for line in dedupe2(f):
				print(line)
		
		
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
