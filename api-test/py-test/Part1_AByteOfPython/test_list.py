#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/14'
Info:
        
"""
import os


if __name__=="__main__":
	try:
		shoplist=['apple','mango','carrot','banana']
		
		# 切片
		print(shoplist[::1]) # ['apple', 'mango', 'carrot', 'banana'] 间隔1个元素
		print(shoplist[::2]) # ['apple', 'carrot'] 0，2
		print(shoplist[::3]) # ['apple', 'banana'] 0，3
		print(shoplist[::-1]) # ['banana', 'carrot', 'mango', 'apple'] 倒序
		
		# 包含
		print('appl' in shoplist)
		print('apple' in shoplist)
		
		# 去重
		shopset = {shoplist}
		
		# 定制排序
		points = [ { 'x' : 8, 'y' : 3 }, { 'x' : 4, 'y' : 1 } ]
		points.sort(key=lambda e:e['x'],reverse=True) # key 对应排序参照,默认升序排列
		print(points)
		
		# 列表推断式
		listone = [2,3,4]
		listtwo = [2*i for i in listone if i > 2] # 守卫 + 倍增
		print(listtwo)
		
	
		
		
		
		
	finally:
		os._exit(0)
	
		






