#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/14'
Info:
        
"""

import os,sys

__version__='0.1'

def printMSG(x,y):
	'''print the max value of two numbers
	hello world.
	'''
	# 函数文档定格写
	
	x=int(x)
	y=int(y)
	print(x,y)
	
	print(max(x,y))


if __name__=="__main__":
	try:
		print(printMSG.__doc__) # 打印显示文档
		printMSG(sys.argv[1],sys.argv[2]) # 入参 0 为脚本名称，从 1 以后开始
	finally:
		os._exit(0)