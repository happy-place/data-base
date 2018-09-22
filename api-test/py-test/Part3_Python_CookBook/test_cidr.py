#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
import ipaddress
from socket import socket,AF_INET,SOCK_STREAM

def test_cidr():
	net = ipaddress.ip_network('123.45.67.64/27')
	print('{!r:}'.format(net)) # IPv4Network('123.45.67.64/27')
	for x in net:
		print(x)
	
	'''
	123.45.67.64
	123.45.67.65
	....
	123.45.67.95
	'''
	
	net6 = ipaddress.ip_network('12:3456:78:90ab:cd:ef01:23:30/125')
	print('{!r:}'.format(net6)) # IPv6Network('12:3456:78:90ab:cd:ef01:23:30/125')
	print(net6.broadcast_address,net6.netmask) # 12:3456:78:90ab:cd:ef01:23:37 ffff:ffff:ffff:ffff:ffff:ffff:ffff:fff8
	for x in net6:
		print(x)
	'''
	12:3456:78:90ab:cd:ef01:23:30
	12:3456:78:90ab:cd:ef01:23:31
	....
	12:3456:78:90ab:cd:ef01:23:37
	'''

def test_index():
	net = ipaddress.ip_network('123.45.67.64/27')
	print(net.num_addresses) # 长度 32
	print('{!r:}'.format(net[2])) # 索引取值 123.45.67.66
	
	# 判断成员是否存在
	a = ipaddress.ip_address('123.45.67.69') # 注意此处ip_address 与 上面 ip_network的区别
	print('{!r:}'.format(a))
	print(a in net)
	
	b = ipaddress.ip_address('123.45.67.123')
	print(b in net)

def test_ip():
	# 通过ip接口指定ip地址和网络地址
	inet = ipaddress.ip_interface('123.45.67.73/27')
	print(inet.network) # 123.45.67.64/27
	print(inet.ip) # 123.45.67.73

def test_tcp():
	# 创建tcp 客户端连接是，需要使用 str()函数封装 IP实例
	a = ipaddress.ip_address('127.0.0.1')
	s = socket(AF_INET,SOCK_STREAM)
	s.connect(str(a),2000)



if __name__=="__main__":
	try:
		# test_cidr()
		# test_index()
		test_ip()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




