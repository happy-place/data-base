#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,sys
from queue import Queue
from functools import wraps


def apply_async(func,args,*,callback):
	'''
	异步函数：先执行 func，然后将程序结果反馈给callback继续处理
	:param func:
	:param args:
	:param callback:
	:return:
	'''
	result = func(*args)
	callback(result)

def print_result(result):
	print('Got: ',result)

def add(x,y):
	return x+y

def test_async():
	apply_async(add,(1,2),callback=print_result)
	apply_async(add,('hello ','world'),callback=print_result)
	'''
	Got:  3
	Got:  hello world
	'''

# 回调函数记录回调顺序

# 方案1：定义类，将类方法传入回调函数作为callback,类属性记录每次回调状态
class ResultHandler:
	def __init__(self):
		self.sequence = 0
	
	def handler(self,result):
		self.sequence +=1
		print('[{}] Got: {}'.format(self.sequence,result))

def stateful_async():
	r = ResultHandler()
	apply_async(add,(1,2),callback=r.handler)
	apply_async(add,('hello ','world'),callback=r.handler)
	'''
	[1] Got: 3
	[2] Got: hello world
	'''

# 方案2：通过函数闭包方式，维护变量记录被闭包函数的调用记录
def handler():
	sequence = 0
	def do(result):
		nonlocal sequence # 先在本地找，然后到外部查找 LEGB local Enclosing Global Build-in
		sequence +=1
		print('[{}] Got: {}'.format(sequence,result))
	return do


def stateful_async2():
	h = handler()
	apply_async(add,(1,2),callback=h)
	apply_async(add,('hello ','world'),callback=h)
	'''
	[1] Got: 3
	[2] Got: hello world
	'''

# 方案3：通过协程实现
def make_handler():
	sequence = 0
	while True:
		result = yield # 每次调用 make_handler.send 就释放一次，否则就阻塞在此
		sequence +=1
		print('[{}] Got: {}'.format(sequence,result))


def stateful_async3():
	m = make_handler()
	next(m) # 启动协程
	apply_async(add,(1,2),callback=m.send)
	apply_async(add,('hello ','world'),callback=m.send)
	'''
	[1] Got: 3
	[2] Got: hello world
	'''

class Async:
	def __init__(self,func,args):
		self.func = func
		self.args = args
	
def inlined_async(func):
	@wraps(func)
	def wrapper(*args):
		f = func(*args)
		result_queue = Queue()
		result_queue.put(None)
		while True:
			result = result_queue.get()
			try:
				a = f.send(result) # 协程
				apply_async(a.func,a.args,callback=result_queue.put)
				
				pass
			except StopIteration:
				break
	return wrapper
		

@inlined_async
def test():
	r = yield Async(add,(2,3))
	print(r)
	r = yield Async(add,('hello ','world'))
	print(r)
	for n in range(10):
		r = yield Async(add,(n,n))
		print(r)
	print('Goodbye')
	
# 访问闭包中的变量
def sample():
	n = 0
	def func():
		print('n=',n)
	
	def get_n():
		return n
	
	def set_n(value):
		nonlocal n  # LEGB
		n = value
	
	func.get_n = get_n # 将 get_n set_n 两个函数都绑定到第三个函数func 上
	func.set_n = set_n
	return func

class ClousureInstance:
	# 获取闭包对象，并将此对象的方法，拆解，封装到字典
	def __init__(self,locals=None):
		if locals is None:
			locals = sys._getframe(1).f_locals
			self.__dict__.update((key,value) for key,value in locals.items() if callable(value))
	
	def __len__(self):
		return self.__dict__['__len__']()

def Stack():
	items = []
	def push(item):
		items.append(item)
	
	def pop():
		return items.pop()
	
	def __len__():
		return len(items)
	
	return ClousureInstance() # 通 sys._getframe(1).f_locals 拿到当前对象所在栈，从而将闭包函数内信息封装到闭包对象中

def test_closuer():
	s = Stack()
	print(s)
	s.push(10)
	s.push(20)
	s.push('hello')
	
	print(len(s))
	print(s.pop())
	print(s.pop())
	print(s.pop())
	
class Stack2:
	def __init__(self):
		self.items = []
	
	def push(self,item):
		self.items.append(item)
	
	def pop(self):
		return self.items.pop()
	
	def __len__(self):
		return len(self.items)
	
	
def compare_stack():
	from timeit import timeit
	'''
	1,    timeit(stmt='pass', setup='pass', timer=<defaulttimer>, number=1000000)
	
	
	       返回：
	
	            返回执行stmt这段代码number遍所用的时间，单位为秒，float型
	
	       参数：
	
	            stmt：要执行的那段代码
	
	            setup：执行代码的准备工作，不计入时间，一般是import之类的
	
	            timer：这个在win32下是time.clock()，linux下是time.time()，默认的，不用管
	
	            number：要执行stmt多少遍
	
	
	
	2,    repeat(stmt='pass', setup='pass', timer=<defaulttimer>, repeat=3, number=1000000)
	
	       这个函数比timeit函数多了一个repeat参数而已，表示重复执行timeit这个过程多少遍，返回一个列表，表示执行每遍的时间
	
	 
	
	当然，为了方便，python还用了一个Timer类，Timer类里面的函数跟上面介绍的两个函数是一样一样的
	
	
	
	class timeit.Timer(stmt='pass', setup='pass',timer=<timer function>)
	
	        Timer.timeit(number=1000000)
	
	        Timer.repeat(repeat=3,number=1000000)
	
	
	'''
    # 从 if __name__=='__main__': 主方法中导入 s1 s2 对象
	t1 = timeit(stmt='s1.push(1);s1.pop()',setup='from __main__ import s1',number=3)
	t2 = timeit(stmt='s2.push(1);s2.pop()',setup='from __main__ import s2',number=3)
	
	print(t1,t2) # 1.271505607292056e-05 1.121999230235815e-05
	pass








if __name__=="__main__":
	try:
		# test_async()
		# stateful_async()
		# stateful_async2()
		# stateful_async3()
		# test()
		
		# f = sample()
		# f.set_n(10)
		# print(f.get_n())
		
		# test_closuer()
		
		s1 = Stack()
		s2 = Stack2()
		compare_stack()
	
		
		
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




