#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
    目前有很多用来实现各种消息传输的包和函数库，比如ZeroMQ、Celery等。 你还有另外一种选择就是自己在底层socket基础之上来实现一个消息传输层。
    但是你想要简单一点的方案，那么这时候 multiprocessing.connection 就派上用场了。 仅仅使用一些简单的语句即可实现多个解释器之间的消息通信。
    
    
    一个通用准则是，你不要使用 multiprocessing 来实现一个对外的公共服务。 Client() 和 Listener() 中的 authkey 参数用来认证发起连接的终端用户。
    如果密钥不对会产生一个异常。此外，该模块最适合用来建立长连接（而不是大量的短连接），
     例如，两个解释器之间启动后就开始建立连接并在处理某个问题过程中会一直保持连接状态。
    
    如果你需要对底层连接做更多的控制，比如需要支持超时、非阻塞I/O或其他类似的特性， 你最好使用另外的库或者是在高层socket上来实现这些特性。
    
"""
import os,traceback
from multiprocessing.connection import Listener

def echo_responser(conn):
	try:
		while True:
			msg = conn.recv()
			conn.send(msg)
	except EOFError:
		print('Connection closed')


def echo_accepter(address,authkey):
	serv = Listener(address,authkey=authkey)
	while True:
		try:
			client = serv.accept()
			echo_responser(client)
		except Exception:
			traceback.print_exc()



def start_server(address):
	print('Listening on {} ... '.format(address))
	echo_accepter(address,authkey=b'peekaboo')


if __name__=="__main__":
	try:
		# start_server(('',20000))
		start_server('/Users/huhao/Desktop/echo.pid')
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




