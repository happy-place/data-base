#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from socket import socket,AF_INET,SOCK_STREAM
from xmlrpc.client import ServerProxy,SafeTransport

import ssl

KEYFILE = '/Users/huhao/privkey.pem' # 私钥
CERTFILE = '/Users/huhao/server_cert.pem' # 公钥

'''
方案1： 直接包装已有 tcp-socket
这种直接处理底层socket方式有个问题就是它不能很好的跟标准库中已存在的网络服务兼容。 例如，绝大部分服务器代码（HTTP、XML-RPC等）实际上是基于
 socketserver 库的。 客户端代码在一个较高层上实现。我们需要另外一种稍微不同的方式来将SSL添加到已存在的服务中：

'''

def echo_client():
	# 创建普通 tcp 连接
	s = socket(AF_INET,SOCK_STREAM)
	# 使用ssl 包装 socket
	s_ssl = ssl.wrap_socket(s,cert_reqs=ssl.CERT_REQUIRED,ca_certs=CERTFILE)
	# 与服务端建立连接
	s_ssl.connect(('localhost',20000))
	# 发送数据
	s_ssl.send(b'hello world?')
	# 8k缓存接受响应
	data = s_ssl.recv(8192)
	print(data)

# 方案2：kv server 将 ssl 和 xmlrpc 混入，直接使用 xmlrpc.client 即可连接(不进过ssl验证)
'''
最近在闲暇时刻看一看Python爬虫，学习到浏览器模拟，对csdn的网页进行抓取，发现报错了。
在网上找了之后发现，原来是 https  引起的。“当使用urllib.urlopen打开一个 https 链接时，会验证一次 SSL 证书。
而当目标网站使用的是自签名的证书时就会抛出此异常。（此处引用，目前还不懂）”
解决办法：
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
'''
def kv_client():
	ssl._create_default_https_context = ssl._create_unverified_context
	
	# s = ServerProxy('https://localhost:20000',allow_none=True)
	s = get_verified_kvserver()
	s.set('foo','bar')
	s.set('spam',[1,2,3])
	print(s.keys)
	print(s.get('spam'))
	s.delete('spam')
	print(s.exists('spam'))


# 需要进过 ssl 验证，基于xmlrpc.client 创建连接
class VerifyCertSafeTransport(SafeTransport):
	def __init__(self, cafile, certfile=None, keyfile=None):
		SafeTransport.__init__(self)
		self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
		self._ssl_context.load_verify_locations(cafile)
		if certfile:
			self._ssl_context.load_cert_chain(certfile, keyfile)
		self._ssl_context.verify_mode = ssl.CERT_REQUIRED
	
	def make_connection(self, host):
		s = super().make_connection(host)
		return s

def get_verified_kvserver():
	s = ServerProxy('https://localhost:20000',transport=VerifyCertSafeTransport(CERTFILE),allow_none=True)
	return s



if __name__=="__main__":
	try:
		# echo_client()
		kv_client()
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




