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
		1/1

	except: # 只在异常发生时运行
		traceback.print_exc()
	
	else: # 只在正常时，运行
		print("no except occured!")

	finally: # 异常 或 正常 都会执行
		os._exit(0)
	