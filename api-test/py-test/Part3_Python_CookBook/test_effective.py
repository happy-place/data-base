#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,urllib.request,cProfile,time
from functools import wraps
from contextlib import contextmanager
from timeit import timeit


# 方案1： time python3 test_effective.py 直接调脚本测试
def fetch():
	u = urllib.request.urlopen('http://www.python.org')
	
	for line in u.readlines():
		# print(line.decode('utf-8'))
		pass
	'''
	real    0m5.562s
	user    0m0.197s
	sys     0m0.051s
	
	'''
	
# 方案2： 直接调用  cProfile.run("fetch()") 打印详细调用信息
def test_cprofile():
	cProfile.run("fetch()")
	'''
	     7839 function calls (7805 primitive calls) in 0.524 seconds
   Ordered by: standard name
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.524    0.524 <string>:1(<module>)
        4    0.000    0.000    0.000    0.000 <string>:12(__new__)
        1    0.000    0.000    0.000    0.000 _collections_abc.py:664(__contains__)
	....
	'''
	
# 方案3：自定义装饰器，统计函数调用时间
def timethis(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		start = time.perf_counter()
		r = func(*args,**kwargs)
		end = time.perf_counter()
		print('{}.{}: {}'.format(func.__module__,func.__name__,end-start))
		return r
	return wrapper

def timethis2(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		start = time.process_time()
		r = func(*args,**kwargs)
		end = time.process_time()
		print('{}.{}: {}'.format(func.__module__,func.__name__,end-start))
		return r
	return wrapper

@timethis # __main__.countdown: 1.592119224369526e-05
# @timethis2 # __main__.countdown: 1.7000000000044757e-05
def countdown(n):
	while n>0:
		n -=1
		
# 方案4：自定义上下文管理器，统计代码块执行效率
@contextmanager
def timeblock(label): # label 为上下文计时器名称
	start = time.perf_counter()
	try:
		yield #此处调用目标函数，带目标函数返回继续向下执行
	finally:
		end = time.perf_counter()
		print('{}: {}'.format(label,end-start))


def testblock():
	with timeblock('counting'): # 统计代码块效率
		n = 100
		while n > 0:
			n -=1

# 方案5：记住现成 timeit 函数，测试函数调用时间
def test_timeit():
	# print(timeit(stmt='math.sqrt(2)',setup='import math')) # 0.285704726818949
	# print(timeit(stmt='sqrt(2)',setup='from math import sqrt')) # 0.1876257830299437
	# 执行1000次，并统计运行时间
	print(timeit(stmt='sqrt(2)',setup='from math import sqrt',number=1000)) # 0.0001478400081396103
	


if __name__=="__main__":
	try:
		countdown(100)
		# test_cprofile()
		# countdown(100) # __main__.countdown: 1.264200545847416e-05
		# testblock() # counting: 1.7281854525208473e-05
		# test_timeit()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




