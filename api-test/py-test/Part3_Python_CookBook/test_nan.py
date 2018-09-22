#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,math


def test_nan():
	'''
	float 中界定了无穷 和 非数字的概念，判定是否为非数字，唯一安全途径就是 math.isnan() 函数
	:return:
	'''
	a = float('inf') # 正无穷
	aa = float('inf')
	b = float('-inf') # 符无穷
	c = float('nan') # not a number
	cc = float('nan')
	
	print(a==aa) # True
	print(a==-b) # True
	print(c==cc,c is cc) # (False, False)
	print(a,b,c) # (inf, -inf, nan)
	print(math.isinf(a),math.isinf(b),math.isinf(c),math.isnan(c)) # (True, True, False, True)
	
	print(c+23,c/2,c*2,math.sqrt(c)) # (nan, nan, nan, nan)
	
	



if __name__=="__main__":
	try:
	
		test_nan()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
