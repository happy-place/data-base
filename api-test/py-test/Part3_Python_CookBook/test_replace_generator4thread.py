#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from collections import deque
from select import select
from socket import socket, AF_INET, SOCK_STREAM
import time

def countdown(n):
	while n>0:
		print('T-minus',n)
		yield
		n -= 1
	print('Blastoff')

# 返回生成器对象
def countup(n):
	x = 0
	while x < n:
		print('Counting up',x)
		yield
		x +=1

class TaskScheduler:
	def __init__(self):
		self._task_queue = deque() # 双向插入队列
	
	def new_task(self,task):
		self._task_queue.append(task) # 右侧插入
	
	# 依次轮询线程队列中注册的生成器
	def run(self):
		while self._task_queue:
			task = self._task_queue.popleft() # 左侧弹出
			try:
				next(task)
				self._task_queue.append(task)
			except StopIteration:
				pass


def test_task():
	sched = TaskScheduler() # sched 中维护了一个线程队列
	sched.new_task(countdown(5)) # 组装线程1
	sched.new_task(countdown(3))  # 组装线程2
	sched.new_task(countup(6))   # 组装线程3
	
	# 启动线程池
	sched.run()
	'''
	T-minus 5
	T-minus 3
	Counting up 0
	T-minus 4
	T-minus 2
	Counting up 1
	T-minus 3
	T-minus 1
	Counting up 2
	T-minus 2
	Blastoff
	Counting up 3
	T-minus 1
	Counting up 4
	Blastoff
	Counting up 5
	'''

class ActorScheduler:
	def __init__(self):
		self._actors = {}
		self._msg_queue = deque() # 实例化双端队列
	
	def new_actor(self,name,actor):
		self._msg_queue.append((actor,None)) # 注册printer 和 counter 对象
		self._actors[name] = actor # 将对象维护到字典
		
	def send(self,name,msg):
		actor = self._actors.get(name) # 获取指定对象，压入队列
		if actor:
			self._msg_queue.append((actor,msg))
		
	def run(self):
		while self._msg_queue: # 一开始启动，队列存在对象，进入循环
			actor,msg = self._msg_queue.popleft() # 按序弹出（右入左出）
			try:
				actor.send(msg) # 调动对象执行相应逻辑
			except StopIteration: # 迭代完成，退出
				pass

def printer():
	# 打印信息生成器
	while True:
		msg = yield
		print('Got:',msg)

def counter(sched):
	while True:
		n = yield # 接受 sched.send('counter',10000) 和 	sched.send('printer',n) 传入参数
		if n == 0:
			break # n=0  while self._msg_queue: 终止
		# 调用打一发，装一发
		sched.send('printer',n)
		sched.send('counter',n-1)
		
def test_actor_scheduler():
	# 创建实例
	sched = ActorScheduler()
	# 往调度器注册 生成器
	sched.new_actor('printer',printer())
	sched.new_actor('counter',counter(sched))
	
	sched.send('counter',10000) # 入参交给 	n = yield
	sched.run()


# This class represents a generic yield event in the scheduler 基类
class YieldEvent:
	def handle_yield(self, sched, task):
		pass
	def handle_resume(self, sched, task):
		pass

# Task Scheduler 调度器
class Scheduler:
	def __init__(self):
		self._numtasks = 0       # Total num of tasks
		self._ready = deque()    # Tasks ready to run
		self._read_waiting = {}  # Tasks waiting to read
		self._write_waiting = {} # Tasks waiting to write
	
	# Poll for I/O events and restart waiting tasks
	def _iopoll(self):
		rset,wset,eset = select(self._read_waiting,
		                        self._write_waiting,[])
		for r in rset: # 轮询读入队列
			evt, task = self._read_waiting.pop(r)
			evt.handle_resume(self, task)
		for w in wset: # 轮询写出队列
			evt, task = self._write_waiting.pop(w)
			evt.handle_resume(self, task)
	
	def new(self,task):
		'''
		Add a newly started task to the scheduler
		'''
		
		self._ready.append((task, None))
		self._numtasks += 1
	
	def add_ready(self, task, msg=None):
		'''
		Append an already started task to the ready queue.
		msg is what to send into the task when it resumes.
		'''
		self._ready.append((task, msg))
	
	# Add a task to the reading set
	def _read_wait(self, fileno, evt, task):
		self._read_waiting[fileno] = (evt, task)
	
	# Add a task to the write set
	def _write_wait(self, fileno, evt, task):
		self._write_waiting[fileno] = (evt, task)
	
	def run(self):
		'''
		Run the task scheduler until there are no tasks
		'''
		while self._numtasks:
			if not self._ready:
				self._iopoll()
			task, msg = self._ready.popleft()
			try:
				# Run the coroutine to the next yield
				r = task.send(msg)
				if isinstance(r, YieldEvent):
					r.handle_yield(self, task)
				else:
					raise RuntimeError('unrecognized yield event')
			except StopIteration:
				self._numtasks -= 1

# Example implementation of coroutine-based socket I/O
class ReadSocket(YieldEvent):
	def __init__(self, sock, nbytes):
		self.sock = sock
		self.nbytes = nbytes
	def handle_yield(self, sched, task):
		sched._read_wait(self.sock.fileno(), self, task)
	def handle_resume(self, sched, task):
		data = self.sock.recv(self.nbytes)
		sched.add_ready(task, data)

class WriteSocket(YieldEvent):
	def __init__(self, sock, data):
		self.sock = sock
		self.data = data
	def handle_yield(self, sched, task):
		
		sched._write_wait(self.sock.fileno(), self, task)
	def handle_resume(self, sched, task):
		nsent = self.sock.send(self.data)
		sched.add_ready(task, nsent)

class AcceptSocket(YieldEvent):
	def __init__(self, sock):
		self.sock = sock
	def handle_yield(self, sched, task):
		sched._read_wait(self.sock.fileno(), self, task)
	def handle_resume(self, sched, task):
		r = self.sock.accept()
		sched.add_ready(task, r)

# Wrapper around a socket object for use with yield
class Socket(object):
	def __init__(self, sock):
		self._sock = sock
	def recv(self, maxbytes):
		return ReadSocket(self._sock, maxbytes)
	def send(self, data):
		return WriteSocket(self._sock, data)
	def accept(self):
		return AcceptSocket(self._sock)
	def __getattr__(self, name):
		return getattr(self._sock, name)

def readline(sock):
	chars = []
	while True:
		c = yield sock.recv(1)
		if not c:
			break
		chars.append(c)
		if c == b'\n':
			break
	return b''.join(chars)
	
	# Echo server using generators
class EchoServer:
	def __init__(self,addr,sched):
		self.sched = sched
		sched.new(self.server_loop(addr))
	
	def server_loop(self,addr):
		s = Socket(socket(AF_INET,SOCK_STREAM))
		
		s.bind(addr)
		s.listen(5)
		while True:
			c,a = yield s.accept()
			print('Got connection from ', a)
			self.sched.new(self.client_handler(Socket(c)))
	
	def client_handler(self,client):
		while True:
			line = yield from readline(client)
			if not line:
				break
			line = b'GOT:' + line
			while line:
				nsent = yield client.send(line)
				line = line[nsent:]
		client.close()
		print('Client closed')

def start_echo():
	sched = Scheduler()
	EchoServer(('',16000),sched)
	sched.run()




if __name__=="__main__":
	try:
		# test_task()
		
		test_actor_scheduler()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




