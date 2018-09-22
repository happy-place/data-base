#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,time
from socket import socket,AF_INET,SOCK_DGRAM

def udp_client():
	s = socket(AF_INET,SOCK_DGRAM)
	code = s.sendto(b'',('localhost',20000))
	print(code)
	
	data = s.recvfrom(8192)
	print(data)
	



if __name__=="__main__":
	try:
		udp_client()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




