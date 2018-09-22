#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from xmlrpc.server import SimpleXMLRPCServer

# 封装类方式暴露rpc 服务
class KeyValueServer:
	_rpc_methods_ = ['get','set','delete','exists','keys']
	
	def __init__(self,address):
		self._data = {}
		self._serv = SimpleXMLRPCServer(address,allow_none=True)
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
	
	def serve_forever(self):
		print('Rpc serving on 20000 ... ')
		self._serv.serve_forever()
	
def start_server1():
	kvserv = KeyValueServer(('',20000))
	kvserv.serve_forever()


# 直接暴露函数方式，运行rpc 服务端
def add(x,y):
	return x + y

def start_server2():
	serv = SimpleXMLRPCServer(('',20000))
	serv.register_function(add)
	serv.serve_forever()






if __name__=="__main__":
	try:
		start_server1()
		# start_server2()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




