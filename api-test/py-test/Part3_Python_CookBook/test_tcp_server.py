#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from time import ctime
import threading
import socket as sc
from socketserver import BaseRequestHandler,TCPServer,StreamRequestHandler,ThreadingTCPServer,ForkingTCPServer,socket



class EchoHandler2(StreamRequestHandler):
	def handle(self):
		print('Got connection from ',self.client_address)
		# 解析接收信息
		data = self.rfile.readline().strip()
		print(data)
		
		# 使用u8编码接收消息，以 utf-8 的响应格式返回
		self.wfile.write(bytes('[%s] %s' % (ctime(),data.decode('utf-8')),'utf-8'))


class EchoHandler(BaseRequestHandler):
	def handle(self):
		print('Got connection from ',self.client_address)
		# 轮询监听
		while True:
			msg = self.request.recv(8192) # 8k 接收信息，并进行处理
			if not msg:
				break
			
			print(threading.current_thread().name)
			self.request.send(msg) # 将收到信息，原样返回
			
			
def test_tcp_server():
	# 只能处理单个客户端请求
	server = TCPServer(('',20000),EchoHandler2) # 启动server ， '' 同绑定 0.0.0.0 的效果一致
	server.serve_forever()


def test_threading_tcp_server():
	# 同时处理多个客户端请求，默认无上限, 很容易遭受饱和攻击
	# serv = ThreadingTCPServer(('',20000),EchoHandler)
	serv = ForkingTCPServer(('',20000),EchoHandler)
	serv.serve_forever()

def test_threadpool():
	'''
	创建容积为16的线程池，真正工作的线程有 16 + 1 主线程，第一个参与服务
	
	:return:
	'''
	NWORKERS = 16
	serv = TCPServer(('',20000),EchoHandler)
	for n in range(NWORKERS):
		t = threading.Thread(target=serv.serve_forever)
		t.daemon = True
		t.start()
		
	serv.serve_forever()      # 阻塞监听


def test_bind_and_activate():
	'''
	通常情况下创建实例同时顺便激活。在此处，创建实例过后并没有立刻激活，而且进行相应的绑定设置，然后激活，最后阻塞提供服务
	'''
	serv = TCPServer(('',20000),EchoHandler,bind_and_activate=False)
	serv.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
	serv.server_bind()
	serv.server_activate()
	serv.serve_forever()


def test_reuse():
	TCPServer.allow_reuse_address = True
	serv = TCPServer(('',20000),EchoHandler)
	serv.serve_forever()


class DefaultSettingEchoHandler(StreamRequestHandler):
	timeout = 5  # 超时设置
	rbufsize = -1  # Read buffer size
	wbufsize = 0   # write buffer size
	disable_nagle_algorithm = False    # 设置 TCP_NODELAY 选项
	
	def handle(self):
		'''
		超过 5s 未接受到数据，会报异常
		
		:return:
		'''
		print('Got connection from ',self.client_address)
		try:
		   	for line in self.rfile:
			    self.wfile.write(line)
		except socket.timeout:
			print('Time out')
	

def test_default_setting():
    serv = TCPServer(('',20000),DefaultSettingEchoHandler)
    serv.serve_forever()
    
    
# 函数方式 创建 tcp 服务器
def echo_handler(client_sock,client_addr):
	print('Got connection from {}'.format(client_addr))
	while True:
		msg = client_sock.recv(8192)
		if not msg:
			break
		client_sock.sendall(msg)
	client_sock.close()


def echo_server(address,backlog=2):
	sock = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
	sock.bind(address)
	sock.listen(backlog) # 只允许 backlog个客户端接入服务器，超过限额，需要排队，队列装不下，则拒绝请求
	
	while True:
		client_sock,client_addr = sock.accept()
		t = threading.Thread(target=echo_handler,args=(client_sock,client_addr))
		t.daemon = True
		t.start()




if __name__=="__main__":
	try:
		# test_tcp_server()
		# test_threading_tcp_server()
		# test_threadpool()
		# test_bind_and_activate()
		# test_reuse()
		# test_default_setting()
		
		echo_server(('',20000))
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




