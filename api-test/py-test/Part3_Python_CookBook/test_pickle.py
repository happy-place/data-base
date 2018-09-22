#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/25'
Info:
        
"""

import os,traceback,pickle,math,threading,time,tempfile

'''
pickle 是一种python特有的自描述的数据编码。通过自描述，被序列化后的数 据包含每个对象开始和结束以及它的类型信息。
因此，你无需担心对象记录的定义，它 总是能工作。举个例子，如果要处理多个对象，你可以这样做:
'''


def save_2_file():
	data = ['1',2,'aa',True]
	with open('tmp.txt','wb') as f:
		pickle.dump(data,f) # python对象序列化到文件
	
	with open('tmp.txt','rb') as f:
		data2 = pickle.load(f) # 从文件还原python对象
		print(type(data2),data2) # <class 'list'> ['1', 2, 'aa', True]
	
	bytes_obj = pickle.dumps(data) # python 对象序列化成二进制字符串
	print(type(bytes_obj),bytes_obj) # <class 'bytes'> b'\x80\x03]q\x00(X\x01\x00\x00\x001q\x01K\x02X\x02\x00\x00\x00aaq\x02\x88e.'
	
	data3 = pickle.loads(bytes_obj) #二进制字符串还原为python对象
	print(type(data3),data3) # <class 'list'> ['1', 2, 'aa', True]


def data_stream():
	# 多次写出
	with open('tmp.txt','wb') as f:
		pickle.dump([1,2,3],f)
		pickle.dump({'name':'tom','age':12},f)
		pickle.dump(True,f)
	
	# 多次读取
	with open('tmp.txt','rb') as f:
		print(pickle.load(f)) # [1, 2, 3]
		print(pickle.load(f)) # {'name': 'tom', 'age': 12}
		print(pickle.load(f)) # True

def serialize_func():
	'''
	千万不 对不信任的数据使用 pickle.load()。
    pickle 在加载时有一个副作用就是它会自动加载相应模块并构建实例对象。
    但是某个坏人如果知pickle.load的工作原理，他就可以创建一个恶意的数据导致python执行恶意指定的系统命令。
    因此一定要包装pickle只在相互之间可以认证对方的解析器的内部使用。
	:return:
	'''
	func_bytes = pickle.dumps(math.sqrt) # 函数序列化成字节字符串
	sqrt = pickle.loads(func_bytes) # 从字节字符串中还原函数
	print(sqrt(4)) # 2.0 会自动加载依赖的模块


class Countdown:
	def __init__(self,n):
		self.n = n # 初始化
		self.thr = threading.Thread(target=self.run) # 线程工作函数 run()
		self.thr.daemon = True # 守护线程
		self.thr.start() # 创建即启动
	
	def run(self):
		while self.n >0: # 计数
			print('T-minus',self.n)
			self.n -= 1
			time.sleep(2)
	
	'''
	有些类型的对象是不能被序列化的。这些通常是那些依赖外部系统状态的对象， 比如打开的文件，网络连接，线程，进程，栈帧等等。
	用户自定义类可以通过提供 __getstate__ 和 __setstate__ 方法来绕过这些限制。如果定义了这两个方法，pickle.dump 就会调用 __getstate__
	获取序列化的对象。类似的, __setstate__ 在反序列化时被调用。
	序列化对象是通过 __getstate__ 保存状态
	反序列化对象时通过 __setstate__ 重新回复状态
	'''
	
	def __getstate__(self): #
		return self.n

	def __setstate__(self,n):
		self.__init__(n)

def test_countdown():
	c = Countdown(30) # 创建子线程类,并直接启动线程

	with open('cnt.txt','wb') as f: # 序列化计数器，此时其实仍然在运行计数
		pickle.dump(c,f)
		
	time.sleep(5) # 主线程休眠
	
	with open('cnt.txt','rb') as f:
		c= pickle.load(f) # 反序列化会计数器，此时总共产生了2份计数器，第一份一直在能运行，第二份从序列化位置开始运行
	
	time.sleep(10)
	
	
	
	
	




if __name__=="__main__":
	try:
		# save_2_file()
		# data_stream()
		# serialize_func()
		test_countdown()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


