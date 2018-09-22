#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from collections import defaultdict
from contextlib import contextmanager

class Exchange:
	'''
	要实现发布/订阅的消息通信模式， 你通常要引入一个单独的“交换机”或“网关”对象作为所有消息的中介。
	也就是说，不直接将消息从一个任务发送到另一个，而是将其发送给交换机， 然后由交换机将它发送给一个或多个被关联任务。
	'''
	def __init__(self):
		self._subscribes = set()
	
	def attach(self,task):
		print('attach ',task)
		self._subscribes.add(task)
	
	def detach(self,task):
		print('detach ',task)
		self._subscribes.remove(task)
	
	def send(self,msg):
		for subsrcibe in self._subscribes:
			subsrcibe.send(msg)


_exchanges = defaultdict(Exchange)


def get_exchange(name):
	return _exchanges[name]


class Task:
	def send(self,msg):
		print(self,' send ',msg)


def test_exc():
	# 创建注册这
	task_a = Task()
	task_b = Task()
	# 创建注册中心 在 defaultdict 中 key 为exc,value 为Exchange 实例的对象
	exc = get_exchange('exc')
	# 往注册中心注册 注册这
	exc.attach(task_a)
	exc.attach(task_b)
	
	# 注册中心 通知注册者，发送消息
	exc.send('msg1')
	exc.send('msg2')
	
	# 注册者解绑
	exc.detach(task_a)
	exc.detach(task_b)


class DisplayMessage:
	'''
	其次，交换机广播消息给多个订阅者的能力带来了一个全新的通信模式。 例如，你可以使用多任务系统、广播或扇出。
	你还可以通过以普通订阅者身份绑定来构建调试和诊断工具。
	'''
	def __init__(self):
		self.count = 0
	
	def send(self,msg):
		print('msg {}: {!r}'.format(self.count,msg))

def test_display():
	try:
		exc =get_exchange('exc')
		d = DisplayMessage()
		exc.attach(d)
		
		# 创建注册这
		task_a = Task()
		task_b = Task()
		# 创建注册中心 在 defaultdict 中 key 为exc,value 为Exchange 实例的对象
		exc = get_exchange('exc')
		# 往注册中心注册 注册这
		exc.attach(task_a)
		exc.attach(task_b)
		
		# 注册中心 通知注册者，发送消息
		exc.send('msg1')
		exc.send('msg2')
	finally:
		# 注册者解绑
		exc.detach(task_a)
		exc.detach(task_b)
		exc.detach(d)
	'''
	attach  <__main__.DisplayMessage object at 0x10f221710>
	attach  <__main__.Task object at 0x10f221748>
	attach  <__main__.Task object at 0x10f221908>
	<__main__.Task object at 0x10f221908>  send  msg1
	msg 0: 'msg1'  << 观察者
	<__main__.Task object at 0x10f221748>  send  msg1
	<__main__.Task object at 0x10f221908>  send  msg2
	msg 0: 'msg2'  << 观察者
	<__main__.Task object at 0x10f221748>  send  msg2
	detach  <__main__.Task object at 0x10f221748>
	detach  <__main__.Task object at 0x10f221908>
	detach  <__main__.DisplayMessage object at 0x10f221710>
	'''


class Exchange2:
	def __init__(self):
		self._subscribes = set()
	
	def attach(self,task):
		self._subscribes.add(task)
	
	def detach(self,task):
		self._subscribes.remove(task)
	
	def send(self,msg):
		for subscribe in self._subscribes:
			subscribe.send(msg)
		
	@contextmanager
	def subscribe(self,*tasks):
		for task in tasks:
			print(self,'attach',task)
			self.attach(task)
		try:
			# do job
			yield
		finally:
			for task in tasks:
				print(self,'detach',task)
				self.detach(task)

_exchanges2 = defaultdict(Exchange2)

def get_exchanges2(name):
	return _exchanges2[name]

def test_exchange2():
	exc = get_exchanges2('exc2')
	
	task_a = Task()
	task_b = Task()
	
	with exc.subscribe(task_a,task_b):
		exc.send('msg1')
		exc.send('msg2')
	'''
	<__main__.Exchange2 object at 0x110167710> attach <__main__.Task object at 0x11014deb8>
	<__main__.Exchange2 object at 0x110167710> attach <__main__.Task object at 0x1101677b8>
	<__main__.Task object at 0x1101677b8>  send  msg1
	<__main__.Task object at 0x11014deb8>  send  msg1
	<__main__.Task object at 0x1101677b8>  send  msg2
	<__main__.Task object at 0x11014deb8>  send  msg2
	<__main__.Exchange2 object at 0x110167710> detach <__main__.Task object at 0x11014deb8>
	<__main__.Exchange2 object at 0x110167710> detach <__main__.Task object at 0x1101677b8>
	
	'''
		


if __name__=="__main__":
	try:
		# test_exc()
		# test_display()
		test_exchange2()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




