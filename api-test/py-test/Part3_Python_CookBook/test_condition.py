#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
    event对象的一个重要特点是当它被设置为真时会唤醒所有等待它的线程。如果你只想唤醒单个线程，最好是使用信号量或者 Condition 对象来替代。
"""
import os,traceback,time,threading
from threading import Thread,Event

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
			# 多个线程节奏一致，就发生阻塞，节奏不一致，就执行操作
			last_flag = self._flag
			while last_flag == self._flag:
				self._cv.wait()


def countdown(nticks):
	while nticks >0:
		ptimer.wait_for_tick() #
		print('T-minus',nticks)
		nticks -=1

def countup(last):
	n = 0
	while n < last:
		ptimer.wait_for_tick()
		print('Counting',n)
		n +=1


if __name__=="__main__":
	try:
		# 通过 ptimer.wait_for_tick() 调用控制节奏
		ptimer = PeriodicTimer(5)
		ptimer.start()
		
		down = threading.Thread(target=countdown,args=(10,))
		up = threading.Thread(target=countup,args=(5,))
		
		down.start()
		up.start()
		
		time.sleep(100)
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




