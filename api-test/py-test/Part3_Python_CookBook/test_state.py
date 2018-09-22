#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
'''
计模式中有一种模式叫状态模式，这一小节算是一个初步入门！
这里看上去有点奇怪，每个状态对象都只有静态方法，并没有存储任何的实例属性数据。
 实际上，所有状态信息都只存储在 Connection 实例中。 在基类中定义的 NotImplementedError
 是为了确保子类实现了相应的方法。 这里你或许还想使用8.12小节讲解的抽象基类方式。
'''
class Connection:
	'''
	普通方案，好多个判断语句，效率
	'''
	def __init__(self):
		self.state = 'CLOSED'
	
	def read(self):
		if self.state != 'OPEN':
			raise RuntimeError('Not open')
		print('reading')
	
	def write(self,data):
		if self.state !='OPEN':
			raise RuntimeError('Not open')
		print('writing',data)
	
	def open(self):
		if self.state == 'OPEN':
			raise RuntimeError('Already open')
		self.state = 'OPEN'
	
	def close(self):
		if self.state == 'CLOSED':
			raise RuntimeError('Already closed')
		self.state = 'CLOSED'
	
	
class Connection1:
	def __init__(self):
		self.new_state(ClosedConnectionState)
	
	def new_state(self,newstate):
		self._state = newstate
	
	def read(self):
		return self._state.read(self)
	
	def write(self,data):
		return self._state.write(self,data)

	def open(self):
		return self._state.open(self)
	
	def close(self):
		return self._state.close(self)
	
	
class ConnectionState:
	@staticmethod
	def read(conn):
		'''委派子类实现'''
		raise NotImplementedError()
	
	@staticmethod
	def write(conn,data):
		'''委派子类实现'''
		raise NotImplementedError()
	
	@staticmethod
	def open(conn):
		'''委派子类实现'''
		raise NotImplementedError()
	
	@staticmethod
	def close(conn):
		'''委派子类实现'''
		raise NotImplementedError()


class ClosedConnectionState(ConnectionState):
	@staticmethod
	def read(conn):
		'''此路不通'''
		raise RuntimeError('Not open')
	@staticmethod
	def write(conn,data):
		raise RuntimeError('Not open')
	@staticmethod
	def open(conn):
		conn.new_state(OpenConnectionState)
	@staticmethod
	def close(conn):
		raise RuntimeError('Already closed')


class OpenConnectionState(ConnectionState):
	@staticmethod
	def read(conn):
		print('reading')
	@staticmethod
	def write(conn,data):
		print('writing',data)
	@staticmethod
	def open(conn):
		raise RuntimeError('Already open')
	@staticmethod
	def close(conn):
		conn.new_state(ClosedConnectionState)


def test_conn():
	c = Connection()
	print(c.state) # CLOSED
	c.open()
	print(c.state) # OPEN
	c.close()
	print(c.state) # CLOSED
	c.open()
	c.write('hi') # writing hi
	c.close()
	
	
def test_conn1():
	c = Connection1() # 创建Connection1实例，并将状态初始化为 ClosedConnectionState，以下操作全部基于ClosedConnectionState 进行
	c.open() # 执行ClosedConnectionState.open(), 状态切换到 OpenConnectionState，以下操作全部在 OpenConnectionState 状态进行
	print(c._state) # 执行 OpenConnectionState._state
	c.write('hello') # writing # 执行 OpenConnectionState.write()
	c.close() # 执行 OpenConnectionState.close()，状态切换到 执行ClosedConnectionState
	
	
	
	
	
	pass
	
	

if __name__=="__main__":
	try:
		# test_conn()
	
		test_conn1()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




