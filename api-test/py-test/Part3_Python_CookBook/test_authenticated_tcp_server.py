#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from socket import socket,AF_INET,SOCK_STREAM
from test_authenticated_tcp import *


def echo_handler(client_sock):
	secret_key = b'peekaboo'
	# 对 socket 进行验签，验签失败，关闭连接
	if not server_authenticate(client_sock,secret_key):
		client_sock.close()
		return
	# 验签成功，接受数据 (8k对齐)
	while True:
		msg = client_sock.recv(8192)
		if not msg: # 接受失败，继续监听
			break
		client_sock.sendall(msg) # 将接收数据直接返回

# ---* 基于解释器层面创建TCP服务端点 *---
def echo_server(address):
	backlog = 5 # 允许等待队列长度
	s = socket(AF_INET,SOCK_STREAM)
	s.bind(address) # tcp 绑定
	s.listen(backlog) # 设置监听队列长度
	# 轮询监听
	while True:
		connection,address = s.accept()
		print('Got connection from {}'.format(address))
		# 将RPC 请求交付处理
		echo_handler(connection)


if __name__=="__main__":
	try:
		echo_server(('',20000))
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




