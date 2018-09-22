#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,threading,time
import urllib.request

# 实例级别上锁，同时间，只能有一个线程操作上锁片段
class ShareCounter:
	def __init__(self,initial_value = 0):
		self._value = initial_value
		self._value_lock = threading.Lock()
	
	# 操作共享资源需要上锁，with 语句能够自发获取锁，和释放锁
	def incr(self,delta=1):
		with self._value_lock:
			print('+',self._value,threading.current_thread().name)
			self._value += delta
	
	def decr(self,delta =1):
		with self._value_lock:
			print('-',self._value,threading.current_thread().name)
			self._value -= delta
	
	# 显示获取锁和释放锁
	def incr1(self,delta=1):
		self._value_lock.acquire()
		print('+',self._value,threading.current_thread().name)
		self._value += delta
		self._value_lock.release()
	
	def decr1(self,delta =1):
		self._value_lock.acquire()
		print('-',self._value,threading.current_thread().name)
		self._value -= delta
		self._value_lock.release()

def do_incr(share):
	while True:
		share.incr()


def do_decr(share):
	while True:
		share.decr()

def test_share():
	s = ShareCounter()

	threading.Thread(target=do_incr,args=(s,),name='01').start()
	threading.Thread(target=do_decr,args=(s,),name='02').start()
	
	time.sleep(5)


# 类级别上锁，同一时间，只能有一个线程，操作完整的对象函数
class ShareCounter:
	
	_rlock = threading.RLock()
	
	def __init__(self,initial_value=0):
		self._value = initial_value
	
	def incr(self,delta=1):
		with ShareCounter._rlock:
			self._value +=delta
	
	def decr(self,delta=1):
		with ShareCounter._rlock:
			self._value -=delta


# 引入信号量Semaphore，控制并发访问量
_fetch_url_sema = threading.Semaphore(2)

def fetch_url(url):
	with _fetch_url_sema: # 同时间只允许_fetch_url_sema个线程访问
		print(threading.current_thread().name)
		return urllib.request.urlopen(url)

def test_sema():
	for i in range(5):
		t = threading.Thread(target=fetch_url,args=('http://www.baidu.com',))
		t.start()
	
	time.sleep(5)
	



if __name__=="__main__":
	try:
		# test_share()
		test_sema()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




