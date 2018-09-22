#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""

import os,traceback,random

def test_choice():
	values = [1,2,3,4,5,6]
	# 获取一个随机数
	print(random.choice(values))
	print(random.choice(values))
	print(random.choice(values))
	
	# 随机取样
	print(random.sample(values,2))
	print(random.sample(values,2))
	print(random.sample(values,3))
	print(random.sample(values,3))
	
	# 混洗 [2, 6, 5, 4, 3, 1]
	random.shuffle(values)
	print(values)
	
	# [0,10] 之间的随机数
	print(random.randint(0,10))
	print(random.randint(0,10))
	print(random.randint(0,10))
	print(random.randint(0,10))
	
	# (0,1) 间随机浮点数
	print(random.random()) # 0.646044943522
	print(random.random())
	print(random.random())
	
	# 获取[1,200] 位随机二进制整数
	v = random.getrandbits(20)
	print(v) # 310294
	print(bin(v)) # 0b1001011110000010110
	
	# 基于系统时间 或 os.urandome() 置随机数种，每次运行得到的随机数肯定不同
	random.seed()
	print(random.randint(0,10))
	
	# 指定整形随机数种，每次运行得到的随机数种肯定相同
	random.seed(12345)
	
	# 指定字符串种，每次运行得到的随机数种肯定相同
	print(random.randint(0,10)) # 4
	print(random.randint(0,10)) # 0
	
	random.seed(b'bytedata')
	print(random.randint(0,10)) # 0
	print(random.randint(0,10)) # 4
	
	
if __name__=="__main__":
	try:
		test_choice()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)





