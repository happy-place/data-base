#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        分数运算
"""

import os,traceback,math
from fractions import Fraction

def test_cal():
	a = Fraction(5,4)
	b = Fraction(7,16)
	print(a+b) # 27/16
	
	c = a*b
	
	print(c,c.numerator,c.denominator) # (Fraction(35, 64), 35, 64) numerator 分子，denominator 分母
	print(float(c)) # 0.546875 分数转换成为小数
	
	d = a**b
	print(Fraction(d).limit_denominator()) # 878334/796639 小数转成分数，得到近似分数值
	
	x = 3.74
	y = Fraction(*x.as_integer_ratio())
	print(y) # 小数转为真分数
	
	
	pass

if __name__=="__main__":
	try:
		test_cal()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)



