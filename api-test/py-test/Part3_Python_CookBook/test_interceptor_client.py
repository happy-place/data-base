#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from multiprocessing.connection import Client

def echo_client(addrsss):
	c = Client(addrsss,authkey=b'peekaboo')
	c.send('hello')
	data = c.recv()
	print(data) # hello
	
	c.send(42)
	data = c.recv()
	print(data) # 42
	
	c.send([1,2,3,4])
	data = c.recv()
	print(data) # [1, 2, 3, 4]
	
	pass




if __name__=="__main__":
	try:
		# echo_client(('localhost',20000)) # 基于套接字，在解释器层面通信
		echo_client('/Users/huhao/Desktop/echo.pid') # 基于管道文件，在解释器层面通信，相应目录会创建管道句柄，但不会真正形成管道文件
		# 解释器版本必须一致，不同版本python 的 pickle 序列化协议不同
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




