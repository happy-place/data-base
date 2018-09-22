#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/16'
Info:
        
"""
import os,traceback


if __name__=="__main__":
	
	try:
		name = "Tom"
		age = 11
		salary = 100.23
		
		# 按序入参
		print("{0},{1},{2}".format(name,age,salary))
	
		# 具名传参
		print("{name},{age},{salary}".format(name=name,age=age,salary=salary))
		
		# int,float 格式化
		print("{0:s},{1:d},{2:3.3f}".format(name,age,salary)) # Tom,11,100.230
		
		# 对齐输出
		print("{0:^11}".format(name)) # 居中对齐，长度为11个字符 '    Tom    '
		print(name.rjust(12,'-')) # 右对齐，字符长度 12 ---------Tom
		print(name.ljust(12,'-')) # 左对齐，字符长度 12 Tom---------
		print(name.center(12,'-')) # 居中对齐，字符长度 12 ----Tom-----
		pass
		
	
	
	
	except:
		traceback.print_exc()
	finally:
		os._exit(0)