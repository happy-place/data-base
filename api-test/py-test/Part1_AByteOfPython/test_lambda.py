#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/17'
Info:
        
"""
import os,traceback

def make_repaeter(n):
	'''返回重复n次函数'''
	return lambda s:s*n




if __name__=="__main__":
	
	try:
		
		twice = make_repaeter(2)
		
		print(twice(5))
		print(twice('a'))
		print(twice([1,2,3]))
		
		points = [ { 'x' : 8, 'y' : 3 }, { 'x' : 4, 'y' : 1 } ]
		points.sort(key=lambda e:e['x'],reverse=True) # key 对应排序参照,默认升序排列
		print(points)
		
		pass
	
	except:
		traceback.print_exc()
	finally:
		os._exit(0)