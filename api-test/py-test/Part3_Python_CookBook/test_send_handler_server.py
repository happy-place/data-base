#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,time,sys
import socket

import struct

def send_fd(sock, fd):
	'''
	Send a single file descriptor.
	'''
	sock.sendmsg([b'x'],
	             [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack('i', fd))])
	ack = sock.recv(2)
	assert ack == b'OK'

def server(work_address, port):
	# Wait for the worker to connect
	work_serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	work_serv.bind(work_address)
	work_serv.listen(1)
	worker, addr = work_serv.accept()
	
	# Now run a TCP/IP server and send clients to worker
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
	s.bind(('',port))
	s.listen(1)
	while True:
		client, addr = s.accept()
		print('SERVER: Got connection from', addr)
		send_fd(worker, client.fileno())
		client.close()


def start_server(host,port):
	server(host,port)


if __name__=="__main__":
	try:
		
		# if len(sys.argv) !=3:
		# 	print('Usage: server.py server_address port',file=sys.stderr)
		# 	raise SystemExit(1)
		
		start_server('/Users/huhao/Desktop/serverconn',20000)
	
	
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




