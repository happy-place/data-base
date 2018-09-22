#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,time,sys
from multiprocessing.connection import Client
from multiprocessing.reduction import recv_handle, send_handle
from socket import socket,AF_INET,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR

import socket
import struct


def recv_fd(sock):
	'''
	Receive a single file descriptor
	'''
	msg, ancdata, flags, addr = sock.recvmsg(1,
	                                         socket.CMSG_LEN(struct.calcsize('i')))
	
	cmsg_level, cmsg_type, cmsg_data = ancdata[0]
	assert cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS
	sock.sendall(b'OK')
	
	return struct.unpack('i', cmsg_data)[0]

def worker(server_address):
	serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	serv.connect(server_address)
	while True:
		fd = recv_fd(serv)
		print('WORKER: GOT FD', fd)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as client:
			while True:
				msg = client.recv(1024)
				if not msg:
					break
				print('WORKER: RECV {!r}'.format(msg))
				client.send(msg)


if __name__=="__main__":
	try:
		
		worker('/Users/huhao/Desktop/serverconn')
	
	
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




