#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/24'
Info:
        
"""
import os,traceback,gzip,bz2
from functools import partial
import os.path


def test_read_from_gzip():
	# text mode 模式读取
	with gzip.open('num.txt.gz','rt') as f:
		text = f.read()
		print(text)
	'''
	1 2 3
	1 c 3
	1 2 3
	1 t 3
	1 2 3
	'''
	with bz2.open('num.txt.bz2','rt') as f:
		text = f.read()
		print(text)
	'''
	1 2 3
	1 c 3
	1 2 3
	1 t 3
	1 2 3
	'''
	
def test_write_to_gzip():
	# text mode 模式（即unicode 编码）写出
	with gzip.open('num.txt.gz','wt') as f:
		f.write('hello world\nhello tom')

	with bz2.open('num.txt.bz2','wt') as f:
		f.write('hello tom')


def test_args():
	'''
	compresslevel 压缩级别，最高位9，级别越高，体积越小，解码性能消耗越高
	encoding 指定解码方式 ，
	errors 异常解析，处理策略"ignore"直接忽略，"replace" 替换
	newLine 默认情况不用填写，会自动替换成对应平台的换行符，newline='' 关闭了自动校正换行符的功能
	:return:
	'''
	
	with gzip.open('num.txt.gz','wt',compresslevel=5) as f:
		f.write('hello world\nhello lucy')
		
	with gzip.open('num.txt.gz','rt',encoding='utf-8',errors="ignore",newline='') as f:
		print(f.read())
	

def test_in_openfile():
	'''
	gzip.open 还可以对接其他已经打开的二进制文件，继续进行处理，此二进制危机可以是 管道文件，套接字，普通打开文件等
	
	:return:
	'''
	try:
		f = open('num.txt.gz','rb')
		with gzip.open(f,'rt') as fg:
			print(fg.read())
	finally:
		f.close()


def test_partial():
	'''
	        对象是一个可迭代对象，它会不断的产生固定大小的数据 块，直到文件末尾。要注意的是如果总记录大小不是块大小的整数倍的话，
	        最后一个返 回元素的字节数会比期望值少
	:return:
	'''
	RECODRD_SIZE = 32
	with open('merged.txt','rb') as f:
		# 注partial 偏函数中传入的是一个函数 f.read
		records = iter(partial(f.read,RECODRD_SIZE),b'') # 迭代终止条件 b'' 与 文件打开方式 rb 需要保持一致
		for rec in records:
			print(rec)
		
def test_buf():
	buf = bytearray(os.path.getsize('merged.txt')) # 创建与文件大小一致的缓冲区
	with open('merged.txt','rb') as f:
		f.readinto(buf) # 数据读入缓冲区，给预先分配了内存的数组填充数据
	# bytearray(b'#!/usr/bin/env python\n# -...)
	
	return buf
	
def write_by_buf():
	record_size = 32
	buf = bytearray(record_size)
	with open('merged.txt','rb') as f:
		while True:
			n = f.readinto(buf) # 数据读入缓冲区，返回读取字节长度
			print(buf)
			if n < record_size: # 最后终止
				break

def test_memory_view():
	buf = bytearray(b'hello world')
	view = memoryview(buf) # 非复制情况下创建视图
	for x in view:
		print(chr(x),end='')
	print(view[-5:])
	print(view[-5:])
	
	view[-5:][:] = b'WORLD' # 替换（基于地址修改值）
	print(buf)



if __name__=="__main__":
	try:
		# test_write_to_gzip()
		# test_read_from_gzip()
		# test_args()
		
		# test_in_openfile()
		# test_partial()
		
		# buf = test_buf()
		# print(test_buf())
		# print(buf[0:5])
		# with open('merged2.txt','wb') as f:
		# 	f.write(buf)
		
		
		# write_by_buf()
		test_memory_view()
		
		
		pass
	
	
	except:
		traceback.print_exc()
	finally:
		os._exit(0)