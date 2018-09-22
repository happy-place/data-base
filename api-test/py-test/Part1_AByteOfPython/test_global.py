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
	global x  # 生命在函数内使用的是全局变量
	x = 100

def func2():
	x = 200 # 函数内使用的是局部变量

if __name__=="__main__":
	print(x)
	func2()
	print(x)
	func1()
	print(x)
	os._exit(0)
# sys.exit(0) # 在此处没用

