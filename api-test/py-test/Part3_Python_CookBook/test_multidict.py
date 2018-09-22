#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""

import os,traceback
from collections import defaultdict

def merge_dict():
	d1 = {'a':1,'b':2}
	d2 = {'a':1,'b':3,'c':3}
	
	d = defaultdict(list)
	
	for k,v in d1.items():
		d[k].append(v)
	
	for k,v in d2.items():
		d[k].append(v)
	
	print(d)


if __name__=="__main__":
	try:
		'''
		multidict：一个key对应多个value
		'''
		# 使用 collections 内置的 defaultdict 实现单键多值映射效果，相同 key 的value 被list 收集，可以维护插入顺序，但不能排重
		d = defaultdict(list)
		d['a'].append(1)
		d['a'].append(2)
		d['a'].append(2)
		d['b'].append(4)
		
		print(d) # defaultdict(<class 'list'>, {'a': [1, 2, 2], 'b': [4]})
		print(d['a']) # [1, 2, 2]
		
		# 可以排重但不能维护插入顺序
		d = defaultdict(set)
		d['a'].add(3)
		d['a'].add(1)
		d['a'].add(2)
		d['a'].add(1)
		d['b'].add(4)
		print(d) # defaultdict(<class 'set'>, {'a': {1, 2, 3}, 'b': {4}})
		
		# 手动实现 defaultdict(list)
		d = dict()
		d.setdefault('a',[]).append(1)
		d.setdefault('a',[]).append(2)
		d.setdefault('b',[]).append(1)
		d.setdefault('a',[]).append(2)
		
		print(d) # {'a': [1, 2, 2], 'b': [1]}
		
		# 手动实现 defaultdict(set)
		d = dict()
		d.setdefault('a',set()).add(1)
		d.setdefault('a',set()).add(2)
		d.setdefault('b',set()).add(1)
		d.setdefault('a',set()).add(2)
		print(d)
		
		merge_dict()
			
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)



