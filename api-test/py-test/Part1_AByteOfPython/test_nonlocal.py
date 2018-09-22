#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/13'
Info:
        
"""
import sys,os

x = 0

def func1():
	x=1
	def func2():
		# x=2
		y=2
		def func3():
			nonlocal x  # 先从本地开始找，然后从上层依次往外剥，直至找到最外层全局环境变量
			print('>>>> {x}'.format(x=x))
		func3()
	func2()


if __name__=="__main__":
	try:
		func1()
	finally:
		os._exit(0)
		
# sys.exit(0) # 在此处没用
