#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""

import os,traceback
from operator import itemgetter

def test_exchange():
	x = 1234
	print(bin(x)) # 0b10011010010
	print(oct(x)) # 0o2322
	print(hex(x)) # 0x4d2
	print(int(bin(x),base=2)) # 1234 base 标记 前面你参数的类型
	print(ord('a')) # 97 char -> ascii
	print(chr(97)) # a ascii -> char

	print(format(x,'b')) # 10011010010
	print(format(x,'o')) # 2322
	print(format(x,'x')) # 4d2
	
	# 无符数值，需要在源数值基础上添加指示最大位长度的值
	print(format(2**32+x,'b')) # 100000000000000000000010011010010
	print(format(2**32+x,'x')) # 1000004d2
	print(int('4b2',16)) # 1202
	print(int('10011010010', 2)) # 1234
	
def test_octal():
	os.chmod('test_attrgetter.py',0o775) # 0o775 是八进制

if __name__=="__main__":
	try:
		# test_exchange()
		test_octal()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)

