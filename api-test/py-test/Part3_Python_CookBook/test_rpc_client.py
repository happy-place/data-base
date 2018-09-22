#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        XML-RPC的一个缺点是它的性能。SimpleXMLRPCServer 的实现是单线程的， 所以它不适合于大型程序，
    尽管我们在11.2小节中演示过它是可以通过多线程来执行的。 另外，由于 XML-RPC 将所有数据都序列化为XML格式，
    所以它会比其他的方式运行的慢一些。 但是它也有优点，这种方式的编码可以被绝大部分其他编程语言支持。 通过使用这种方式，
    其他语言的客户端程序都能访问你的服务。
		虽然XML-RPC有很多缺点，但是如果你需要快速构建一个简单远程过程调用系统的话，它仍然值得去学习的。 有时候，简单的方案就已经足够了。
"""
import os,traceback
from xmlrpc.client import ServerProxy

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

def rpc_client1():
	s = ServerProxy('http://localhost:20000',allow_none=True)
	
	s.set('foo','bar')
	s.set('spam',[1,2,3])
	
	keys = s.keys()
	print(keys) # ['foo', 'spam']
	
	foo = s.get('foo')
	print(foo) # bar
	
	s.delete('spam')
	
	exist = s.exists('spam')
	print(exist) # False
	
	# rpc 处理自定义的对象时，只有字典部分数据被处理
	s.set('point',Point(1,2))
	p = s.get('point')
	print(p) # {'x': 1, 'y': 2}
	
	s.set('bin',b'hello world')
	bin = s.get('bin')
	print('{!r:}'.format(bin)) # <xmlrpc.client.Binary object at 0x10d578e48>
	print('{!s:}'.format(bin)) # hello world 自动转码
	
	
def rpc_client2():
	s = ServerProxy('http://localhost:20000',allow_none=True)
	
	res = s.add(1,2)
	print(res) # 3
	
	res = s.add('aa','bb')
	print(res) # aabb


def rpc_client2():
	s = ServerProxy('http://localhost:20000',allow_none=True)
	
	res = s.add(1,2)
	print(res) # 3
	
	res = s.add('aa','bb')
	print(res) # aabb



if __name__=="__main__":
	try:
		rpc_client1()
		# rpc_client2()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




