#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/17'
Info:
        
"""

import os,traceback


if __name__=="__main__":
	'''
	repr 可将python 对象转换成标准 str 输出
	通过eval 可以将 str 还原成指定匹配个数对象
	exec 更多是偏计算，数据出来过程
	'''
	try:
		
		d3 = ["我",'你']
		print(repr(d3)) # list 对象 转为了 str
		print(eval(repr(d3))[1])
		
	
	
		pass
	
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
