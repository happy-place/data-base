#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,time,socket,multiprocessing
from threading import Thread

def countdown(n):
	while n>0:
		print('T-minus',n)
		n -=1
		time.sleep(2)

def start():
	# 创建一个线程，target 为目标函数，args 为入参，默认是 集合类型
	t = Thread(target=countdown,args=(3,),name='child-01')
	# 启动线程
	t.start()
	
	# 监控线程生命状态
	while True:
		if t.is_alive():
			print('Still running')
			time.sleep(1)
		else:
			print('Completed')
			break
	

class CountdownTask:
	def __init__(self):
		self._running = True
	
	def terminate(self):
		self._running = False
	
	def awake(self):
		self._running = True
	
	def run(self,n):
		while n >0:
			if self._running:
				print('T-minus',n)
				n -=1
			time.sleep(2)

def test_join():
	# 创建线程实现类
	c = CountdownTask()
	# 创建线程实例
	t = Thread(target=c.run,args=(3,))
	# 启动线程
	t.start()
	# 暂停线程，并休眠 3s
	c.terminate()
	print('terminate for 3 seconds ...')
	time.sleep(3)
	# 唤醒线程
	c.awake()
	# 阻塞主进程
	t.join() # 暂停当前主线程，等待 t 结束，在继续向下执行，相当于 阻塞功能
	print('over')


class IOTask:
	def terminate(self):
		self._running = False
	
	def run(self,sock):
		sock.settimeout(5)
		while self._running:
			try:
				# IO 现场监护人那个阻塞过程，如果 sock 断开，线程将永久被阻塞，此时需要使用 超时循环操作线程
				data = sock.recv(8192)
				break
			except socket.timeout:
				continue
	
# 继承方式创建线程实例
class CountdownThread(Thread):
	def __init__(self,n):
		super().__init__()
		self.n = n
	
	def run(self):
		while self.n>0:
			print('T-minus',self.n)
			self.n -=1
			time.sleep(2)

def start_thread():
	c = CountdownThread(3)
	c.start()
	c.join() # 阻塞
	

# 通过multiprocessing 模块创建多线程
def start_thread2():
	c = CountdownTask()
	p = multiprocessing.Process(target=c.run,args=(3,))
	p.start()
	p.join()

	
if __name__=="__main__":
	try:
		# start()
		# test_join()
		# start_thread()
		start_thread2()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




