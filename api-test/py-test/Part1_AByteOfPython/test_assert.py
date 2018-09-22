#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/17'
Info:
        
"""

import os,traceback


if __name__=="__main__":
	
	try:
		
		l1 = [1,2,3]
		
		a = 1
		assert a in l1  # 满足条件直接向下执行，否则报错
		print(a)
		
		a = 4
		assert a in l1  # AssertionError
		print(a)
		
		pass
	
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
