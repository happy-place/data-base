#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,queue,socket,os,select,threading,time

# 基于socket 构建通信队列，q1,q2,q3 共享服务端点，存入消息，然后统一由服务端点吐出消息
class PollableQueue(queue.Queue):
	def __init__(self):
		super().__init__()
		if os.name == 'posix':
			self._putsocket,self._getsocket = socket.socketpair()
		else:
			server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			server.bind(('127.0.0.1',0))
			server.listen(1)
			self._putsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self._putsocket.connect(server.getsockname())
			self._getsocket,_ = server.accept()
			server.close()
		
	def fileno(self):
		return self._getsocket.fileno()
	
	def put(self, item):
		super().put(item)
		self._putsocket.send(b'x')
	
	def get(self):
		self._getsocket.recv(1)
		return super().get()
	
		
def consumer(queues):
	while True:
		# 轮询多个队列，并执行消费
		can_read,_,_ = select.select(queues,[],[])
		for r in can_read:
			item = r.get()
			print('Got:',item)
		
def start_queue():
	q1 = PollableQueue()
	q2 = PollableQueue()
	q3 = PollableQueue()
	
	t = threading.Thread(target=consumer,args=([q1,q2,q3],))
	t.daemon = True
	t.start()
	
	q1.put(1)
	q2.put(10)
	q3.put('hello')
	
	q2.put(15)
	
	time.sleep(2)


def event_loop(sockets,queues):
	while True:
		can_read,_,_ = select.select(sockets,[],[],0.01)
		for r in can_read: # 轮询 socket-queue
			item = r.get()
			print('Got:',item)
		for q in queues: # 轮询队列
			if not q.empty():
				item = q.get()
				print('Got:',item)
		



if __name__=="__main__":
	try:
		start_queue()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




