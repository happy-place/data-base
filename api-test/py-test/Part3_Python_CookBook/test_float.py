#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/20'
Info:
        
"""

import os,traceback,math
from decimal import Decimal,localcontext

def test_round():
	# 标准四舍五入
	print(round(1.23,1)) # 1.2
	print(round(1.27,1)) # 1.3
	print(round(-1.23,1)) # -1.2
	print(round(-1.27,1)) # -1.3
	print(round(1.23345,3)) # 1.233
	
	# 正好处于中间 取离它最近的偶数
	print(round(2.5,0)) # 2.0
	print(round(1.5,0)) # 2.0
	
	# 接受负数时，直接擦除指定位数
	print(round(123456,-1)) # 123460
	print(round(123456,-2)) # 123500
	print(round(123456,-3)) # 123000

def test_sum():
	nums = [1.28e+18,1,-1.28e+18]
	print(sum(nums)) # 0.0
	print(math.fsum(nums)) # 1.0
	




def test_decimal():
	# 金融领域禁止通过 round 四舍五入方式解决浮点运算精度问题
	a = 2.1
	b = 4.3
	print(a+b) # 6.300000000000001
	print(round(a+b,2)) # 6.3
	
	# 常用的解决办法是 万能字符串 str + Decimal
	a = Decimal('2.1')
	b = Decimal('4.3')
	c = a + b
	print(c) # 6.3
	
	# 通过localcontext 可自行控制精度
	with localcontext() as ctx:
		ctx.prec = 3
		print(a/b) #  0.488
		
	with localcontext() as ctx:
		ctx.prec = 50
		print(a/b) #  0.48837209302325581395348837209302325581395348837209




def test_format():
	'''
	'[<>^]?width[,]?(.digits)?'
	[...]? 可选 < 做对齐 > 右对齐 width 宽 , 33对齐逗号分隔，.digits 小数点位数（指定四舍五入）
	
	:return:
	'''
	x = 12345.6789
	print(format(x,'0.2f')) # 12345.68
	print(format(x,'0.3f')) # 12345.679
	print('value is {:0.3f}'.format(x)) # value is 12345.679
	print(format(x,'>10.1f')) # '   12345.7'
	print(format(x,'<10.1f')) # '12345.7   '
	print(format(x,'^10.1f')) # ' 12345.7  '
	print(format(x,',')) # 12,345.6789
	print(format(x,'e')) # 1.234568e+04
	print(format(x,'0.3e')) # 1.235e+04
	print(format(x,'0,.2f')) # 12,345.68

	swap_dict = {ord('.'):',',ord(','):'.'} # 小数点与逗号功能互换
	print(format(x,',').translate(swap_dict)) # 12.345,6789
	
	print('%0.2f'%x) # '12345.68'
	print('%10.2f'%x) # '  12345.68'
	print('%-10.2f'%x) # '12345.68  '
	

if __name__=="__main__":
	try:
		# test_round()
		# test_format()
		# test_decimal()
		# test_sum()
		test_format()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)



