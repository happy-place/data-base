#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,time,threading
from threading import Thread,Event

def countdown(n,started_evt):
	print('countdown starting')
	while n >0:
		print('T-minus',n)
		n -=1
		time.sleep(2)
	started_evt.set()

def test_evt():
	started_evt = Event()
	print('Launching countdown ...')
	t = Thread(target=countdown,args=(5,started_evt))
	t.start()
	started_evt.wait() # 阻塞直至 evt 所在线程 执行了evt.set() 操作，才放行，继续向下执行
	print('countdown is over ...')
	'''
	Launching countdown ...
	countdown starting
	T-minus 10
	countdown is running ...
	'''

class PeriodicTimer:
	def __init__(self,interval):
		self._interval = interval
		self._flag = 0
		self._cv = threading.Condition()
		
	def start(self):
		t = threading.Thread(target=self.run)
		t.daemon = True
		t.start()
	
	def run(self):
		while True:
			time.sleep(self._interval)
			with self._cv:
				self._flag ^= 1
				self._cv.notify_all()
	
	def wait_for_tick(self):
		with self._cv:
			last_flag = self._flag
			while last_flag == self._flag:
				self._cv.wait()

def start_timer():
	ptimer = PeriodicTimer(3)
	ptimer.start()




if __name__=="__main__":
	try:
		# test_evt()
		start_timer()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




