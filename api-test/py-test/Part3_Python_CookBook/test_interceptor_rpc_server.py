#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
    在一个消息传输层如 sockets 、multiprocessing connections 或 ZeroMQ 的基础之上实现一个简单的远程过程调用（RPC）。
"""
import os,traceback,pickle,json
from multiprocessing.connection import Listener
from threading import Thread

# ----* 内聚逻辑与外部RPC服务对接 *----
def rpc_server(handler,address,authkey):
	# 创建基于 python 解释器的RPC 通信服务器
	sock = Listener(address,authkey=authkey)
	print('Rpc serving on {} ... '.format(address[1]))
	
	# 轮询监听 RPC 请求
	while True:
		# 提取客户端连接
		client = sock.accept()
		# 将客户端连接交给内聚逻辑链路(多线程处理请求)
		t = Thread(target=handler.handle_connection,args=(client,))
		t.daemon = True # 守护执行（复用）
		t.start()

# ----* 普通业务函数 *----
def add(x,y):
	return x+y

def sub(x,y):
	return x - y

# ----* RPC 对外接收器与对内路由执行器对接函数 *----
def start_server():
	# 向对内路由执行器注册业务函数
	handler = RPCHandler()
	handler.register_function(add)
	handler.register_function(sub)
	
	# 将内聚逻辑链路交给对外接收器
	rpc_server(handler,('localhost',20000),authkey=b'peekaboo')
	


class RPCHandler:
	def __init__(self):
		self._functions = {}
	
	def register_function(self,func):
		self._functions[func.__name__] = func
	
	def handle_connection(self,connection):
		try:
			while True:
				# 反序列化 rpc 客户端传入的 数据
				func_name, args,kwargs = pickle.loads(connection.recv())
				try:
					# 对目标函数进行调用
					res = self._functions[func_name](*args,**kwargs)
					# 将运算结果序列化，然后返回
					connection.send(pickle.dumps(res))
				except Exception as e:
					# 出现异常，照常将异常序列化，然后返回
					connection.send(pickle.dumps(e))
		except EOFError:
			pass
	
	
class RPCJSONHandler:
	def __init__(self):
		self._functions = {}

	def register_function(self,func):
		self._functions[func.__name__] = func
	
	def handle_connection(self,connection):
		try:
			while True:
				# 反序列化 rpc 客户端传入的 数据
				func_name, args,kwargs = json.loads(connection.recv())
				try:
					# 对目标函数进行调用
					res = self._functions[func_name](*args,**kwargs)
					# 将运算结果序列化，然后返回
					connection.send(json.dumps(str(res)))
				except Exception as e:
					# 出现异常，照常将异常序列化，然后返回
					connection.send(json.dumps(str(e)))
		except EOFError:
			pass


# ----* RPC 对外接收器与对内路由执行器对接函数 *----
def start_json_server():
	# 向对内路由执行器注册业务函数
	handler = RPCJSONHandler()
	handler.register_function(add)
	handler.register_function(sub)
	
	# 将内聚逻辑链路交给对外接收器
	rpc_server(handler,('localhost',20000),authkey=b'peekaboo')





if __name__=="__main__":
	try:
		# start_server()
		start_json_server()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




