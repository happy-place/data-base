#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
    在一个消息传输层如 sockets 、multiprocessing connections 或 ZeroMQ 的基础之上实现一个简单的远程过程调用（RPC）。
    
    Client(RPCProxy) => Listener(RPCHandler)
    
    RPCHandler 和 RPCProxy 的基本思路是很比较简单的。 如果一个客户端想要调用一个远程函数，比如 foo(1, 2, z=3) ,代理类创建一个包含了函数名和参数的元组 ('foo', (1, 2), {'z': 3}) 。 这个元组被pickle序列化后通过网络连接发生出去。 这一步在 RPCProxy 的 __getattr__() 方法返回的 do_rpc() 闭包中完成。 服务器接收后通过pickle反序列化消息，查找函数名看看是否已经注册过，然后执行相应的函数。 执行结果(或异常)被pickle序列化后返回发送给客户端。我们的实例需要依赖 multiprocessing 进行通信。 不过，这种方式可以适用于其他任何消息系统。例如，如果你想在ZeroMQ之上实习RPC， 仅仅只需要将连接对象换成合适的ZeroMQ的socket对象即可。

由于底层需要依赖pickle，那么安全问题就需要考虑了 （因为一个聪明的黑客可以创建特定的消息，能够让任意函数通过pickle反序列化后被执行）。 因此你永远不要允许来自不信任或未认证的客户端的RPC。特别是你绝对不要允许来自Internet的任意机器的访问， 这种只能在内部被使用，位于防火墙后面并且不要对外暴露。

作为pickle的替代，你也许可以考虑使用JSON、XML或一些其他的编码格式来序列化消息。 例如，本机实例可以很容易的改写成JSON编码方案。还需要将 pickle.loads() 和 pickle.dumps() 替换成 json.loads() 和 json.dumps() 即可：
	
	注：不管序列化逻辑变成 pickle 还是 json ，最终直接拿到的结果仍维持原始类型
    
"""
import os,traceback,pickle,json
from multiprocessing.connection import Client

# 直接返回结果
class RPCProxy:
	def __init__(self,connection):
		self._connection = connection
	
	def __getattr__(self, name):
		def do_rpc(*args,**kwargs):
			self._connection.send(pickle.dumps((name,args,kwargs)))
			result = pickle.loads(self._connection.recv())
			if isinstance(result,Exception):
				raise result
			return result
		return do_rpc


def rpc_client():
	# 创建基于 python 解释器的 客户端通信端点
	c = Client(('localhost',20000),authkey=b'peekaboo')
	# 使用RPC协议包装通信端点
	proxy = RPCProxy(c)
	# 基于RPC代理，完成对目标函数调用
	result = proxy.add(2,3) # 底层实质是调用 __getattr__，异常将 目标方法名，参数，序列化，通过 解释器通信客户端传出，完成调用
	print(result)
	
	result = proxy.sub(2,3)
	print(result)
	
	result = proxy.add([1,2],3)
	print(result)

# 返回json
class RPCJSONProxy:
	def __init__(self,connection):
		self._connection = connection
	
	def __getattr__(self, name):
		def do_rpc(*args,**kwargs):
			self._connection.send(json.dumps((name,args,kwargs)))
			result = json.loads(self._connection.recv())
			if isinstance(result,Exception):
				raise result
			return result
		return do_rpc

def rpc_json_client():
	# 创建基于 python 解释器的 客户端通信端点
	c = Client(('localhost',20000),authkey=b'peekaboo')
	# 使用RPC协议包装通信端点
	proxy = RPCJSONProxy(c)
	# 基于RPC代理，完成对目标函数调用
	result = proxy.add(2,3) # 底层实质是调用 __getattr__，异常将 目标方法名，参数，序列化，通过 解释器通信客户端传出，完成调用
	print(result)
	
	result = proxy.sub(2,3)
	print(result)
	
	result = proxy.add([1,2],3)
	print(result)




if __name__=="__main__":
	try:
		# rpc_client()
		rpc_json_client()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)







