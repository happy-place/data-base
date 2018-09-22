#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from queue import Queue
from threading import Thread,Event

class ActorExit(Exception):
	pass

class Actor:
	def __init__(self):
		self._mainbox = Queue()
	
	def send(self,msg):
		self._mainbox.put(msg)
	
	def recv(self):
		msg = self._mainbox.get()
		if msg is ActorExit:
			raise ActorExit()
		return msg
	
	def close(self):
		self.send(ActorExit)
	
	def start(self):
		self._terminated = Event()
		t = Thread(target=self._bootstrap)
		t.daemon = True
		t.start()
	
	def _bootstrap(self):
		try:
			self.run()
		except ActorExit: # close -> ActorExit -> recv -> raise ActorExit() -> ._terminated.set() 释放阻塞
			pass
		finally:
			self._terminated.set()
	
	def join(self):
		self._terminated.wait()
	
	def run(self):
		while True:
			msg = self.recv()


class PrintActor(Actor):
	def run(self):
		while True:
			msg = self.recv()
			print('Got: ',msg)


def test_actor():
	p = PrintActor()
	p.start() # 启动actor
	p.send('hello')
	p.send('world')
	p.close() # 停止发送消息
	p.join() # 阻塞，等待返回结果


# 如果你放宽对于同步和异步消息发送的要求， 类actor对象还可以通过生成器来简化定义
def print_actor():
	while True:
		try:
			msg = yield      # Get a message
			print('Got:', msg)
		except RuntimeError:
			print('Actor terminating')


def test_print():
	p = print_actor()
	next(p)
	p.send('hello')
	p.send('world')
	p.close()
	
'''
actor模式的魅力就在于它的简单性。 实际上，这里仅仅只有一个核心操作 send() . 甚至，
对于在基于actor系统中的“消息”的泛化概念可以已多种方式被扩展。
'''
class TaggedActor(Actor):
	def run(self):
		while True:
			tag,*payload = self.recv()
			getattr(self,'do_'+tag)(*payload)
	
	def do_A(self,x):
		print('Running A',x)

	def do_B(self,x,y):
		print('Running B',x,y)

def test_actor2():
	a = TaggedActor()
	a.start()
	a.send(('A',1))
	a.send(('B',2,3))
	a.close()
	a.join()


class Result:
	def __init__(self):
		self._evt = Event()
		self._result = None
	
	def set_result(self, value):
		self._result = value
		
		self._evt.set()
	
	def result(self):
		self._evt.wait()
		return self._result

class Worker(Actor):
	def submit(self, func, *args, **kwargs):
		r = Result()
		self.send((func, args, kwargs, r)) # 分配相应函数执行计算逻辑
		return r # 返回结果
	
	def run(self):
		while True:
			func, args, kwargs, r = self.recv() # 接受请求
			r.set_result(func(*args, **kwargs)) # 调用，并唤醒阻塞，返回结果
			
			
def test_worker():
	worker = Worker()
	worker.start() # 启动 actor
	r = worker.submit(pow,2,3)
	print(r.result()) # 阻塞
	worker.close()




if __name__=="__main__":
	try:
		# test_actor()
		# test_print()
		
		# test_actor2()
		test_worker()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




