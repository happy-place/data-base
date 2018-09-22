#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from socket import socket,AF_INET,SOCK_STREAM


def client_4_stream_req():
	while True:
		# 创建连接
		s=socket(AF_INET, SOCK_STREAM)
		s.connect(('localhost',20000))
		
		# 接收控制台消息，并将字符转换成为字节，发送出去
		data=input('> ')
		
		# u8编码字符消息
		s.send(bytes(data+"\n", encoding = "utf8"))
		
		# 接收回执消息 8k 对齐
		feedback = s.recv(8192)
		
		# 接收失败，则断开否则轮询从控制台读入消息，再发射出去
		if not feedback:
			break
		
		# 打印接收的回执消息
		print(feedback,'utf-8')
		
		# 关闭流
		s.close()


def client_4_base_req():
	# 启动客户端
	s = socket(AF_INET,SOCK_STREAM)
	s.connect(('localhost',20000))
	
	while True:
		# 接收控制台消息，并将字符转换成为字节，发送出去
		data=input('> ')
		
		# u8编码字符消息
		s.send(bytes(data+"\n", encoding = "utf8"))
	
		resp = s.recv(8192) # 接收返回消息
		print(resp) # b'hello'
	
	s.close()








if __name__=="__main__":
	try:
		client_4_base_req()
		# client_4_stream_req()

		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




