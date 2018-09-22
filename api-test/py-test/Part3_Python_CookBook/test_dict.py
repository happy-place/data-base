#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/19'
Info:
        
"""

import os,traceback,math
from operator import itemgetter
from itertools import compress



'''
itemgetter从dict 取出指定 key 进行排序

'''

def get_sub():
	prices = {
		'ACME': 45.23,
		'AAPL': 612.78,
		'IBM': 205.55,
		'HPQ': 37.20,
		'FB': 10.75
		}
	
	# 基于value 提取kv
	p1 = {key:value for key,value in prices.items() if value>200}
	print(p1) # {'AAPL': 612.78, 'IBM': 205.55}
	
	# 提取指定key 对应的 kv 字典推导式过滤子集比 dict() 构造器创建爱子集效率更高，可读性也较好
	teach_name = {'AAPL','IBM','HPQ','HSFT'}
	p2 = {key:value for key,value in prices.items() if key in teach_name}
	print(p2) # {'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.2}
	
	p4 = {key:prices[key] for key in prices.keys() & teach_name}
	print(p4) # {'AAPL': 612.78, 'HPQ': 37.2, 'IBM': 205.55}
	
	p3 = dict((key,value) for key,value in prices.items() if value>200)
	print(p3) # {'AAPL': 612.78, 'IBM': 205.55}


if __name__=="__main__":
	try:
		get_sub()
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


