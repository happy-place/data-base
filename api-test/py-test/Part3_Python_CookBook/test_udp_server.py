#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
	UDP 无需三次握手，提前建立连接通道，大数据信息，直接封装数据包发送，容易丢包
	适合对传输可靠性要求不是很高的场合，如多媒体流以及游戏领域， 无需返回恢复丢失的数据包（程序只需简单的忽略它并继续向前运行）。
"""
import os,traceback,time
import socket
from socketserver import BaseRequestHandler,UDPServer

class TimeHandler(BaseRequestHandler):
	def handle(self):
		print('Got connection from ',self.client_address)
		msg,sock = self.request
		resp = time.ctime()
		sock.sendto(resp.encode('ascii'),self.client_address)


def test_udp_server():
	serv = UDPServer(('',20000),TimeHandler)
	serv.serve_forever()


# 函数式 udp 服务端编程
def time_server(address):
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind(address)
	while True:
		msg,addr = sock.recvfrom(8192)
		print('Got msg from ',addr)
		resp = time.ctime()
		sock.sendto(resp.encode('ascii'),addr)








if __name__=="__main__":
	try:
		# test_udp_server()
		time_server(('',20000))
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




