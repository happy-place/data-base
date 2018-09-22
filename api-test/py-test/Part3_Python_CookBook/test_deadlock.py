#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,threading,time
from contextlib import contextmanager

_local = threading.local()


@contextmanager
def acquire(*locks):
	# Sort locks by object identifier
	locks = sorted(locks, key=lambda x: id(x))
	
	# Make sure lock order of previously acquired locks is not violated
	acquired = getattr(_local,'acquired',[])
	if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
		raise RuntimeError('Lock Order Violation')
	
	# Acquire all of the locks
	acquired.extend(locks)
	_local.acquired = acquired
	
	try:
		for lock in locks:
			lock.acquire()
		yield
	finally:
		# Release locks in reverse order of acquisition
		for lock in reversed(locks):
			lock.release()
		del acquired[-len(locks):]


x_lock = threading.Lock()
y_lock = threading.Lock()

def thread_1():
	while True:
		with acquire(x_lock,y_lock):
			print('Thread-1')

def thread_2():
	while True:
		with acquire(y_lock,x_lock):
			print('Thread-2')

def test_acquire():
	t1 = threading.Thread(target=thread_1)
	t1.daemon = True
	t1.start()
	
	t2 = threading.Thread(target=thread_2)
	t2.daemon = True
	t2.start()
	
	


if __name__=="__main__":
	try:
		test_acquire()
		time.sleep(5)
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




