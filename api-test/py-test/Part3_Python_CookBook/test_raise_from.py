#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

def test_raise_from():
	try:
		int('N/A')
	except ValueError as e:
		raise RuntimeError('A parsing error occured') from e
		# raise E from e 可以同时记录上下层异常信息， 通过 raise E from None 斩断链条
	'''
	ValueError: invalid literal for int() with base 10: 'N/A'
	The above exception was the direct cause of the following exception:
	...
	RuntimeError: A parsing error occured
	'''


def test_cause():
	try:
		int('N/A')
	except Exception as e:
		raise RuntimeError('A parsing error occured') from e
		
	

if __name__=="__main__":
	try:
		# test_raise_from()
		test_cause()
		pass
	except Exception as e:
		print('Cause: ',e.__cause__) # 通过 e.__cause__ 追踪依赖链条Cause:  invalid literal for int() with base 10: 'N/A'
	finally:
		os._exit(0)




