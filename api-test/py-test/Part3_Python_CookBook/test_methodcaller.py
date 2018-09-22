#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
import math,operator

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	
	def __repr__(self):
		return 'Point({!r:},{!r:})'.format(self.x,self.y)
	
	def distance(self,x,y):
		return math.hypot(self.x - x,self.y - y)

def test_caller():
	'''简单反射调用 getattr'''
	p = Point(2,3)
	d1 = getattr(p,'distance')(0,0)
	print(d1)
	
	'''高级反射调用'''
	d2 = operator.methodcaller('distance',0,0)(p)
	print(d2)
	
	points = [Point(1,2),Point(3,0),Point(10,-3),Point(-5,-7),Point(-1,8),Point(3,2)]
	
	points.sort(key=operator.methodcaller('distance',0,0)) # 多次调用
	# [Point(1,2), Point(3,0), Point(3,2), Point(-1,8), Point(-5,-7), Point(10,-3)]基于到目标点距离排序
	print(points)
	
	d1 = operator.methodcaller('distance',0,0) #  求任一点到（0，0） 的距离
	print(d1(Point(1,1))) # 1.4142135623730951
	
	
	
	
	
	


if __name__=="__main__":
	try:
		test_caller()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




