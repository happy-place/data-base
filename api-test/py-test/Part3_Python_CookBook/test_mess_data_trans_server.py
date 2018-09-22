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


def start_server():
	s = socket(AF_INET,SOCK_STREAM)
	s.bind(('',25000))
	s.listen(1)
	dest,addr = s.accept()
	
	arr = numpy.arange(0.0,50000000.0)

	send_from(arr,dest)


if __name__=="__main__":
	try:
		start_server()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




