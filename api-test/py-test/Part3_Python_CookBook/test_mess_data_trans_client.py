#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
	演示服务端 借助 memoryview 往客户端发送大数据集
"""
import os,traceback
from test_mess_data_trans import *
from socket import *
import numpy


def client_server():
	c = socket(AF_INET,SOCK_STREAM)
	c.connect(('localhost',25000))
	a = numpy.zeros(shape=50000000,dtype=float)
	print(a[0:10])
	view = recv_into(a,c)



if __name__=="__main__":
	try:
		client_server()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




