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
		exec("print('hello world')")
		
		a = 1
		print(id(a),a)
		exec('a = 3 * 2')  # 执行赋值操作
		print(id(a),a)
		
		
		eval('print("hello")')
		b = eval('2*3') # eval 默认有返回值，可直接对变量进行赋值
		print(b)
		
	
		pass
	
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
