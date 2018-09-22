#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/17'
Info:
        
"""

import os,traceback,json


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
		
		d1 = {'a':1,'b':2}
		s2 = json.dumps(d1)  # dict 序列化成 str
		
		d2 = eval(s2) # 将字符串还原成 对象，此处相当于 json.loads(s2)
		print(s2)
		print(d2['a'])
	
		d3 = ["我",'你']
		print(repr(d3)) # list 对象 转为了 str
		print(eval(repr(d3))[1])
		
		pass
	
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
