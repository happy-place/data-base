#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,hmac
from socket import socket,AF_INET,SOCK_STREAM
from test_authenticated_tcp import *


def test_client():
	secret_key = b'peekaboo'
	s = socket(AF_INET,SOCK_STREAM)
	s.connect(('localhost',20000))
	client_authenicate(s,secret_key)

	s.send(b'Hello world')
	resp = s.recv(1024)
	print(resp)
	
	s.send(b'Hello tom')
	resp = s.recv(1024)
	print(resp)
	
	

if __name__=="__main__":
	try:
		test_client()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




