#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from socket import socket,AF_INET,SOCK_STREAM
from functools import partial


class LazyConnection:
	'''
	能被 with 语句 调用前提是包含 __enter__ __exit__ 函数
	'''
	def __init__(self,address,family=AF_INET,type=SOCK_STREAM):
		self.address = address
		self.family = family
		self.type = type
		self.sock = None
	
	def __enter__(self):
		'''
		只能创建一个连接
		:return:
		'''
		if self.sock is not None:
			raise RuntimeError('Already connected')
		self.sock = socket(self.family,self.type)
		self.sock.connect(self.address)
		return self.sock

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.sock.close()
		self.sock = None

def test_with1():
	conn = LazyConnection(('www.python.org',80)) # 创建 http 连接
	
	with conn as s: # 进入with语句在，自动执行 __enter__ 创建了连接
		s.send(b'GET /index.html HTTP/1.0\r\n') # 请求资源
		s.send(b'Host: www.python.org\r\n') # 请求地址
		s.send(b'\r\n')
		resp = b''.join(iter(partial(s.recv,8192),b'')) # 每次接受8192字节
		print(resp) # b'HTTP/1.1 301 Moved Permanently\r\nServer: Varnish\r\nRetry-After: 0\r\nLocation: https://www.python.org/index.html\r\nContent-Length: 0\r\nAccept-Ranges: bytes\r\nDate: Tue, 31 Jul 2018 08:56:39 GMT\r\nVia: 1.1 varnish\r\nConnection: close\r\nX-Served-By: cache-hkg17932-HKG\r\nX-Cache: HIT\r\nX-Cache-Hits: 0\r\nX-Timer: S1533027400.892625,VS0,VE0\r\nStrict-Transport-Security: max-age=63072000; includeSubDomains\r\n\r\n'
	# 出with语句，自动执行 __exit__ 即便发生异常也会执行


class LazyConnection2:
	'''
	能被 with 语句 调用前提是包含 __enter__ __exit__ 函数
	'''
	def __init__(self,address,family=AF_INET,type=SOCK_STREAM):
		self.address = address
		self.family = family
		self.type = type
		self.connections = []
		
	def __enter__(self):
		self.sock = socket(self.family,self.type)
		self.sock.connect(self.address)
		self.connections.append(self.sock)
		return self.sock
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.connections.pop().close()


def test():
	
	conn = LazyConnection2(('www.python.org', 80)) # 懒加载模式，此时并没有创建对象
	
	with conn as s1:
		# 创建了第一个 conn 对象，并加入了connections 集合
		s1.send(b'GET /index.html HTTP/1.0\r\n') # 请求资源
		s1.send(b'Host: www.python.org\r\n') # 请求地址
		s1.send(b'\r\n')
		resp = b''.join(iter(partial(s1.recv,8192),b'')) # 每次接受8192字节
		print(resp)
		print(len(conn.connections)) # 1
		
		with conn as s2:
			# 创建了第二个 conn 对象，并加入了connections 集合
			s2.send(b'GET /index.html HTTP/1.0\r\n') # 请求资源
			s2.send(b'Host: www.python.org\r\n') # 请求地址
			s2.send(b'\r\n')
			resp = b''.join(iter(partial(s2.recv,8192),b'')) # 每次接受8192字节
			print(resp)
			print(len(conn.connections)) # 2


if __name__=="__main__":
	try:
		# test_with1()
		test()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




