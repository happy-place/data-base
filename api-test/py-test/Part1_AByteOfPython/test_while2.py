#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/13'
Info:
        
"""
import traceback,os


if __name__=="__main__":
	try:
		while True:
			s = raw_input("please enter something: ")
			if s == "quit":
				break  # 正常退出
			if len(s) < 3:
				print("too small")
				
			print("Input '{s}' is of sufficent length".format(s=s))
			
			continue # 返回继续执行,continue 之后的代码永远不会被执行
			
		else:  # 正常退出时执行
			print("over")
	except:
		traceback.print_exc()  # 异常堆栈
	finally:
		os._exit(0)  # 退出
	