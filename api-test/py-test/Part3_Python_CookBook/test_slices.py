#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback
from collections import defaultdict



if __name__=="__main__":
	try:
		'''
		slices 定义切片
		'''
		record = '....................100 .......513.25 ..........'
		
		# 通过定义切片，截取字符串，打到见名知意效果
		SHARES = slice(20,23)
		PRICE = slice(31,37)
		
		# cost = int(record[20:23]) * float(record[31:37])
		cost = int(record[SHARES])*float(record[PRICE])
		print(cost) # 51325.0
		
		items = [0,1,2,3,4,5,6]
		a = slice(2,4,1)
		
		print(a.start,a.stop,a.step) # 2 4 1 为指定步长,默认为1
		print(items[a]) # 等效与 items[2:4] [2, 3]
		
		items[a] = [10,11] # 基于切片进行赋值 [0, 1, 10, 11, 4, 5, 6]
		print(items)
		
		del items[a] # 删除切片指向位置 [0, 1, 4, 5, 6]
		print(items)
		
		
		a = slice(5,50,2)
		s = 'helloworld'
		print(a.start,a.stop,a.step) # 5 50 2
		a.indices(len(s)) # 通过 indices可对齐相同起点，让切片自动适应新迭代对象收缩(只会收缩，不会扩展)
		print(a.start,a.stop,a.step) # 5 10 2
		
		for i in range(*a.indices(len(s))): # 等效于 range(5,10,2)
			print(s[i])
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
		
		
		