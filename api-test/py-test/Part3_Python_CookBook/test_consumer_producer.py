#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
	Queue 对象已经包含了必要的锁，所以你可以通过它在多个线程间多安全地共享数据。 当使用队列时，协调生产者和消费者的关闭问题可能会有一些麻烦。
一个通用的解决方法是在队列中放置一个特殊的值，当消费者读到这个值的时候，终止执行。
        
"""
import os,traceback,time,heapq,threading
from queue import Queue


def producer(out_q):
	for i in range(5):
		out_q.put(i)
		time.sleep(2)
	out_q.put('over')


def consumer(in_q):
	while True:
		data = in_q.get()
		print(data)
		
		if data == 'over':
			in_q.put(data) # 如果存在多个消费者，此时需要将停止信号，放回
			break

def do_start():
	q = Queue()
	t1 = threading.Thread(target=producer,args=(q,))
	t2 = threading.Thread(target=consumer,args=(q,))
	t1.start()
	t2.start()
	
	t2.join() # 当前主进程阻塞，等待t2完毕

# 优先级队列
class PriorityQueue:
	def __init__(self):
		self._queue = []
		self._count = 0
		self._cv = threading.Condition()
	
	def put(self,item,priority):
		with self._cv:
			heapq.heappush(self._queue,(-priority,self._count,item)) # 存放 优先级，当前索引，对象
			self._count +=1
			self._cv.notify() # 唤醒阻塞线程，可以消费了
	
	def get(self):
		with self._cv:
			while len(self._queue) == 0: # 如果队列为空，则执行阻塞
				self._cv.wait()
			return heapq.heappop(self._queue)[-1] # 消费队列中优先级最高的对象
	

def priority_producer(out_q):
	for i in [3,2,5,1,2]:
		out_q.put(i,i)
		if i>5:
			time.sleep(2)
	out_q.put('over',0)

def priority_consumer(in_q):
	while True:
		data = in_q.get()
		print(data)
		if data == 'over': break
	
def test_proiority():
	q = PriorityQueue()
	t1 = threading.Thread(target=priority_producer,args=(q,))
	t2 = threading.Thread(target=priority_consumer,args=(q,))
	
	t1.start()
	t2.start()
	
	t2.join()


# task_done put 一次，get 一次，然后仔细 task_done() ,q.join() 才会解除阻塞
def task_producer(out_q):
	out_q.put([1,2,3])
	

def task_consumer(in_q):
	data = in_q.get()
	for i in data:
		print(i)
	in_q.task_done()


def test_task():
	q = Queue()
	t1 = threading.Thread(target=task_producer,args=(q,))
	t2 = threading.Thread(target=task_consumer,args=(q,))
	
	t1.start()
	t2.start()

	q.join()

# event ， 生产一个消费一个
def evt_producer(out_p):
	for i in range(3):
		evt = threading.Event()
		out_p.put((i,evt))
		print('put ',i)
		evt.wait()

def evt_consumer(in_q):
	for i in range(3):
		data,evt = in_q.get()
		print('get ',data)
		time.sleep(2)
		evt.set()

def test_evt():
	q = Queue()
	t1 = threading.Thread(target=evt_producer,args=(q,))
	t2 = threading.Thread(target=evt_consumer,args=(q,))
	
	t1.start()
	t2.start()
	
	t2.join()



if __name__=="__main__":
	try:
		# do_start()
		# test_proiority()
		# test_task()
		test_evt()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




