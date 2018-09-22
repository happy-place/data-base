#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,dis

def countdown(n):
	while n >0:
		print('T-minus ',n)
		n -= 1
	print('over!')
	
def test_dis():
	# print(dis.dis(countdown))
	print(countdown.__code__.co_code)


if __name__=="__main__":
	try:
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




