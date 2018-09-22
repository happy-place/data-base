#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
	1.创建ssl 加密服务
	 openssl req -new -x509 -days 365 -nodes -out server_cert.pem
    注：在创建证书的时候，各个值的设定可以是任意的，但是”Common Name“的值通常要包含服务器的DNS主机名。
    如果你只是在本机测试，那么就使用”localhost“，否则使用服务器的域名。

	2.生成加密文件位置 /Usert/yourname/privkey.pem 私钥(KEYFILE),/Usert/yourname/server_cert.pem 公钥(CERTFILE)
	
"""
import os,traceback
from socket import socket,AF_INET,SOCK_STREAM
from xmlrpc.server import SimpleXMLRPCServer
import ssl


KEYFILE = '/Users/huhao/privkey.pem'
CERTFILE = '/Users/huhao/server_cert.pem'

#
'''
方案1： 直接包装已有 tcp-socket
这种直接处理底层socket方式有个问题就是它不能很好的跟标准库中已存在的网络服务兼容。 例如，绝大部分服务器代码（HTTP、XML-RPC等）实际上是基于
 socketserver 库的。 客户端代码在一个较高层上实现。我们需要另外一种稍微不同的方式来将SSL添加到已存在的服务中：

'''
def echo_back(s):
	# 8k对齐，轮询接受数据，然后执行响应
	while True:
		data = s.recv(8192)
		if data == b'':
			break
		s.send(data) # 每次接受，最长8k字节，接受完毕立即返回，并关闭连接
	s.close()
	print('Connection closed')


def echo_server(address):
	backlog = 1 # 允许同时监听数
	s = socket(AF_INET,SOCK_STREAM) # 创建普通 socket
	s.bind(address) # 绑定监听地址
	s.listen(backlog)  # 执行监听
	
	s_ssl = ssl.wrap_socket(s,keyfile=KEYFILE,certfile=CERTFILE,server_side=True) # 对 socket 通道进行ssl加密
	
	# 轮询接受请求
	while True:
		try:
			# 获取监听客户端代理对象，和客户端地址
			client,address = s_ssl.accept()
			print('Got connection',client,address)
			# 接受客户端发送过来的数据，并执行响应
			echo_back(client)
		except Exception as e:
			print('{}: {}'.format(e.__class__.__name__,e))
	
	
	
# 方案2：
class SSLMixin:
	
	def __init__(self,*args,keyfile=None,certfile=None,ca_certs = None,cert_reqs=ssl.CERT_NONE,**kwargs):
		self._keyfile = keyfile
		self._certfile = certfile
		self._ca_certs = ca_certs
		self._cert_reqs = cert_reqs
		super().__init__(*args,**kwargs)
	
	def get_request(self):
		client,addr = super().get_request()
		client_ssl = ssl.wrap_socket(client,keyfile=self._keyfile,certfile=self._certfile,ca_certs=self._ca_certs,cert_reqs=self._cert_reqs,server_side=True)
		return client_ssl,addr
	
	
class SSLSimpleXMLRPCServer(SSLMixin, SimpleXMLRPCServer):
	pass


class KeyValueServer:
	_rpc_methods_ = ['get','set','delete','exists','keys']
	
	def __init__(self,*args,**kwargs):
		self._data = {}
		self._serv = SSLSimpleXMLRPCServer(*args,allow_none=True,**kwargs)
		for name in self._rpc_methods_:
			self._serv.register_function(getattr(self,name))
	
	def get(self,name):
		return self._data[name]

	def set(self,name,value):
		self._data[name] = value
	
	def delete(self,name):
		del self._data[name]
		
	def exists(self,name):
		return name in self._data
	
	def keys(self):
		return list(self._data)
	
	def server_forever(self):
		self._serv.serve_forever()


def kv_server():
	kvserver = KeyValueServer(('localhost',20000),keyfile=KEYFILE,certfile=CERTFILE)
	kvserver.server_forever()


	
if __name__=="__main__":
	try:
		# echo_server(('',20000))
		kv_server()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




