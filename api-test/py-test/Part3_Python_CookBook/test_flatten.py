#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""

import os,traceback,math
from collections import Iterable

def flatten(items,ignore_types=(str,bytes)):
	for x in items:
		# 是可迭代对象，并且不属于忽略类型(字符串，字节型字符串)
		if isinstance(x,Iterable) and not isinstance(x,ignore_types):
			yield from flatten(x)
			'''
			此处 yield from 等价于
			for xx in flatten(x):
				yield xx
			'''
		else:
			yield x





if __name__=="__main__":
	try:
		items = [1,[2,3],['a','b',['aa','bb']]]
		for x in flatten(items):
			print(x)
			
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




