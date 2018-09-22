#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,urllib.request,threading
from socket import AF_INET,SOCK_STREAM,socket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from queue import Queue

'''
限制线程执行栈大小
如果你加上这条语句并再次运行前面的创建2000个线程试验， 你会发现Python进程只使用到了大概210MB的虚拟内存，而真实内存使用量没有变。
注意线程栈大小必须至少为32768字节，通常是系统内存页大小（4096、8192等）的整数倍。

'''
threading.stack_size(65535)

def echo_client(sock, client_addr):
	'''
	Handle a client connection
	'''
	print('Got connection from', client_addr)
	while True:
		msg = sock.recv(65536)
		if not msg:
			break
		sock.sendall(msg)
	print('Client closed connection')
	sock.close()

def echo_server(addr):
	pool = ThreadPoolExecutor(128)
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind(addr)
	sock.listen(5)
	while True:
		client_sock, client_addr = sock.accept()
		# echo_client 调用函数，函数入参client_sock, client_addr
		pool.submit(echo_client, client_sock, client_addr)

# 手动创建线程池: 生产者  + Queue + 消费者
def echo_client2(q):
	sock,client_addr = q.get()
	print('Got connection from ',client_addr)
	while True:
		msg = sock.recv(65536)
		if not msg:
			break
		sock.sendall(msg)
	print('Client closed connection')
	sock.close()
	
def echo_server2(addr,nworkers):
	q = Queue()
	# 创建了nworkers个消费者，与生产者通过Queue() 进行沟通，生产者负责接收连接，消费者，负责响应
	for n in range(nworkers):
		t = Thread(target=echo_client2,args=(q,))
		t.daemon = True
		t.start()
		
	sock = socket(AF_INET,SOCK_STREAM)
	sock.bind(addr)
	sock.listen(5)
	
	while True:
		client_sock,client_addr = sock.accept()
		q.put((client_sock,client_addr))

# 从 ThreadPoolExecutor 中获取子线程计算结果
def fetch_url(url):
	u = urllib.request.urlopen(url)
	data = u.read()
	return data

def test_submit():
	pool = ThreadPoolExecutor(10)
	a = pool.submit(fetch_url,'http://www.python.org')
	b = pool.submit(fetch_url,'http://www.baidu.com')
	
	x = a.result() # 一直阻塞直至获得结果
	y = b.result()
	print(x)
	print(y)


if __name__=="__main__":
	try:
		# echo_server(('',15000)) # telnet localhost 15000 模拟客户端
		
		# echo_server2(('',15000),128)
		
		test_submit()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




