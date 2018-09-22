#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/24'
Info:
        
"""
import os,traceback,sys
from socket import socket,AF_INET,SOCK_STREAM

'''
需要重点强调的一点是，上面的例子仅仅是为了演示内置的open()函数的一个特 性，并且也只适用于基于Unix的系统。
如果你想将一个类文件接口作用在一个套接字 并希望你的代码可以跨平台，请使用套接字对象的makefile()方法。
但是如果不考虑 可移植性的话，那上面的解决方案会比使用makefile()性能更好一点。
'''
def echo_client(client_socket,addr):
	print('Got connection from ',addr)
	client_in = open(client_socket.fileno(),'rt',encoding='latin-1',closefd=False)
	client_out = open(client_socket.fileno(),'wt',encoding='latin-1',closefd=False)
	
	for line in client_in:
		client_out.write(line)
		client_out.flush()
	client_socket.close()

def echo_server(addr):
	sock = socket(AF_INET,SOCK_STREAM)
	sock.bind(addr)
	sock.listen(1)
	while True:
		client,addr = socket.accept()
		echo_client(client,addr)

def test_open():
	'''
	open 函数实现流重定向输出
	:return:
	'''
	with open(sys.stdout.fileno(),'wb',closefd=False) as bstdout:
		bstdout.write(b'hello world\n')
		bstdout.flush()
		




if __name__=="__main__":
	try:
		# echo_server(('127.0.0.1',9000))
		test_open()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




