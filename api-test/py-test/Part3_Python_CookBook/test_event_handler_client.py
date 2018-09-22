#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from socket import *

def event_client():
	# 创建UDP socket
	s = socket(AF_INET,SOCK_DGRAM)
	# handlers = [UDPTimeServer(('',14000)),UDPEchoServer(('',15000))]
	sendlen = s.sendto(b'',('localhost',14000))
	data = s.recvfrom(128)
	print(data)
	
	sendlen = s.sendto(b'Hello',('localhost',15000))
	data = s.recvfrom(128)
	print(data)


def start_client3():
	# 创建普通 sock
	sock = socket(AF_INET, SOCK_DGRAM)
	for x in range(40):
		# 发送数据 到指定端点
		sock.sendto(str(x).encode('ascii'), ('localhost', 16000))
		# 接收响应，并执行打印
		resp = sock.recvfrom(8192)
		print(resp[0])
		



		
if __name__=="__main__":
	try:
		# event_client()
		start_client3()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




