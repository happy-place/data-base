#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,time
from contextlib import contextmanager

@contextmanager
def timethis(label):
	start = time.time()
	try:
		yield
	finally:
		end = time.time()
		print('{}: {}'.format(label,end - start))

def test_mamager(n):
	'''
	yield 之前的语句 充当 with 语句的 __enter__ 函数，之后的语句充当 __exit__函数
	:return:
	'''
	with timethis('counting'):
		while n > 0:
			n -= 1

@contextmanager
def list_transaction(org_list):
	'''
	模式事务原子性工作原理
	:param org_list:
	:return:
	'''
	working = list(org_list) # 拷贝事务执行前状态
	yield working  #事务执行中
	org_list[:] = working # 事务正常执行，提交，保存新状态


def test_tx():
	items = [1,2,3]
	
	# 正常执行事务
	with list_transaction(items) as working:
		working.append(4)
		working.append(5)
	
	print(items) # [1, 2, 3, 4, 5]
	
	# 模拟事务执行失败，回滚
	try:
		with list_transaction(items) as working:
			working.append(6)
			working.append(7)
			raise RuntimeError('runtime error in tx')
	finally:
		print(items) # [1, 2, 3, 4, 5]


class timethis2:
	'''
	正常情况下定义一个上下文管理器，需要定义 __enter__ 和 __exit__ 方法，使用 @contextmanager 可以更为快捷获取相同效果
	'''
	def __init__(self,label):
		self.label = label
	
	def __enter__(self):
		self.start = time.time()
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		end = time.time()
		print('{}: {}'.format(self.label,end - self.start))


def test_timethis2(n):
	with timethis2('counting'):
		while n > 0:
			n -= 1


if __name__=="__main__":
	try:
		
		# test_mamager(10)
		# test_tx()
		test_timethis2(10)
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




