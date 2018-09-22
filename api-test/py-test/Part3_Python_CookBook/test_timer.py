#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,time

class Timer:
	'''
	 使用 time.time() 或 time.clock() 计算的时间精度因操作系统的不同会有所不同。
	  而使用 time.perf_counter() 函数可以确保使用系统上面最精确的计时器。
	'''
	def __init__(self,func=time.perf_counter):
		self.elapsed = 0.0
		self._func = func
		self._start = None
	
	def start(self):
		if self._start is not None:
			raise RuntimeError('Already started')
		self._start = self._func()
	
	def stop(self):
		if self._start is None:
			raise RuntimeError('Not started')
		end = self._func()
		self.elapsed += end - self._start
		self._start = None
	
	def reset(self):
		self.elapsed = 0.0
	
	@property
	def running(self):
		return self._start is not None
		
	def __enter__(self):
		self.start()
		return self
	
	def __exit__(self, *args):
		self.stop()

def countdown(n):
	while n >0:
		n -=1

def test_timer():
	t = Timer()
	t.start()
	countdown(1000)
	t.stop()
	print(t.elapsed) # 0.0001069169957190752
	
	t.reset() # 重置
	with t:
		countdown(1000)
	print(t.elapsed) # 0.00013717380352318287
	
	with Timer() as t2:
		countdown(1000)
	print(t2.elapsed) # 0.0001414769794791937
	
	with Timer(time.process_time) as t3:
		countdown(1000)
	print(t3.elapsed) # 0.00012500000000004174



if __name__=="__main__":
	try:
		test_timer()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




