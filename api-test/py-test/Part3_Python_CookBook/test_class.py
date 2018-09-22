#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

from datetime import date

_formats = {
	'ymd' : '{d.year}-{d.month}-{d.day}',
	'mdy' : '{d.month}/{d.day}/{d.year}',
	'dmy' : '{d.day}/{d.month}/{d.year}'
	}


class Pair:
	'''
	自定义 __repr__() 和 __str__() 通常是很好的习惯，因为它能简化调试和实例输出。
	__repr__() 生成的文本字符串标准做法是需要让 eval(repr(x)) == x 为真
	'''
	def __init__(self,x,y):
		self.x = x
		self.y = y
	
	def __repr__(self):
		return 'Pair({0.x!r},{0.y!r})'.format(self)

	def __str__(self):
		return '({0.x!s},{0.y!s})'.format(self)

def test_repr():
	p = Pair(3,4)
	print(p.__repr__()) # Pair(3,4) 构造对象

	print(p) # 打印信息

	print('p is {0!r}'.format(p)) # p is Pair(3,4) !r 表明调用 __repr() 函数代替 __str__() 输出
	print('p is {0!s}'.format(p)) # p is (3,4) !s 表明调用 __str__() 输出，是默认配置
	print('p is {0}'.format(p)) # p is (3,4)



class Date:
	def __init__(self,year,month,day):
		self.year = year
		self.month = month
		self.day = day
	
	def __format__(self, code):
		if code == '':
			code = 'ymd'
		fmt = _formats[code]
		return fmt.format(d=self)
		

def test_date():
	d = Date(2018,9,10)
	print(format(d))
	print(format(d,'mdy')) # format() 先调用 class 自身的 __format__() ，如果没有则调用内置的 format
	'''
	2018-9-10
	9/10/2018
	'''
	
	d2 = date(2018,9,10)
	print(format(d2)) # # 2018-09-10
	print(format(d2,'%A, %B, %d, %Y')) # Monday, September, 10, 2018,datetime 模块 内置格式化
	

if __name__=="__main__":
	try:
		# test_repr()
		test_date()
		
		
		os.path.normpath()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




