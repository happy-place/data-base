#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,threading
from socket import socket,AF_INET,SOCK_STREAM
from functools import partial


class LazyConnection:
	def __init__(self,address,family=AF_INET,type=SOCK_STREAM):
		self.address = address
		self.family = family
		self.type = type
		self.local = threading.local()
	
	# 每个连接对象，被with调用，会自动注册到当前所在线程的 thread.local 线程变量中，离开 with 语句，调用 __exit__ 删除
	def __enter__(self):
		if hasattr(self.local,'sock'):
			raise RuntimeError('Already connected')
		self.local.sock = socket(self.family,self.type)
		self.local.sock.connect(self.address)
		return self.local.sock
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.local.sock.close()
		del self.local.sock


def test(conn):
	with conn as s:
		s.send(b'GET /index.html HTTP/1.0\r\n')
		s.send(b'Host: www.python.org\r\n')
		
		s.send(b'\r\n')
		resp = b''.join(iter(partial(s.recv,8192),b''))
		
	print('Got {} bytes'.format(len(resp)))


def start():
	conn = LazyConnection(('www.python.org',80))
	
	t1 = threading.Thread(target=test,args=(conn,))
	t2 = threading.Thread(target=test,args=(conn,))
	
	t1.start()
	t2.start()
	
	t1.join()
	t2.join()


if __name__=="__main__":
	try:
		start()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




