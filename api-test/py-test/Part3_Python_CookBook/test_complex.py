#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""

import os,traceback,sys,cmath

# 强制在 python 2 环境适应 numpy
if sys.version_info[0] !=2:
	print('numpt module need python3.x!')
	os._exit(0)
else:
	import numpy as np


def test_cal():
	a = complex(2,4)
	b = 3 - 5j
	print(a,b) # (2+4j) (3-5j)
	print(a+b) # (5-1j)  实部 虚部 对应相加减
	
	print(a,a.real,a.imag,a.conjugate()) # 复数，实部，虚部 共轭虚数 2.0 4.0 (2-4j)
	print(a*b) # (26+2j) = 2*3 + 2*(-5j) + 4j*3 + 4j*(-5j) = 6+20+(-10+12)j = 26+2j
	print(a/b) # (2+4j)/(3-5j) = (2+4j)*(3+5j)/(3-5j)*(3+5j) = (6-20)+(10+12)j/(9-(-25)) = -14/34 + 22/34j = (-0.4117647058823529+0.6470588235294118j)
	
	# 对复数进行复杂函数运算
	print(cmath.sin(a)) # (24.83130584894638-11.356612711218174j)
	print(cmath.cos(a)) # (-11.36423470640106-24.814651485634187j)
	print(cmath.exp(a)) # (-4.829809383269385-5.5920560936409816j)
	
	
	print(cmath.sqrt(-1)) # 1j math.sqrt(-1)不能进行此运算
	
	pass


def test_np():
	'''
	基于numpy 构建复数数组
	
	:return:
	'''
	a = np.array([2+3j,4+5j,6-7j,8+9j])
	print(a) # # [ 2.+3.j  4.+5.j  6.-7.j  8.+9.j]
	print(a+2) # [  4.+3.j   6.+5.j   8.-7.j  10.+9.j]
	print(np.sin(a))
	'''
	[    9.15449915  -4.16890696j   -56.16227422 -48.50245524j
    -153.20827755-526.47684926j  4008.42651446-589.49948373j]
	'''


if __name__=="__main__":
	try:
		test_cal()
		# test_np()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)





