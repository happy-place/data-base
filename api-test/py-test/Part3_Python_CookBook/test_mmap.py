#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/24'
Info:
        
"""

import os,traceback,mmap

def memory_map(filename,access=mmap.ACCESS_WRITE):
	'''
	直接通过操作文件映射的内存区域操作文件内容
	
	
	:param filename:
	:param access:
	:return:
	'''
	size = os.path.getsize(filename)
	fd = os.open(filename,os.O_RDWR)
	return mmap.mmap(fd,size,access=access)
	
def test_memory_map():
	try:
		mp = memory_map('merged.txt')
		print(len(mp)) # 总字节长度 7844
		print(mp[0],chr(mp[0])) # 35 #
		print(mp[0:10]) # b'#!/usr/bin'
		
	finally:
		mp.close()
	
	
def test_write():
	# mmap 只能对已经存在的文件进行操作
	filename = 'nu.txt'
	data = b'hello world\nhello python\n'
	size = len(data) # 通过mmap 写入文件的内容长度，不得超过原始内容长度(mmap实质是覆盖操作)
	
	# ----------- 初始化一个定长文件，等待被mmap 操作 ---------------
	
	with open(filename,'wb') as f:
		f.seek(size-1)
		f.write(b' ')
		f.flush()
		f.close()
	
	# ----------- 基于mmap覆盖写入 ---------------
	
	with memory_map(filename,access=mmap.ACCESS_WRITE) as mp:
		mp.write(data)
		mp[-3:] = b'123'
		mp.flush()
	
	# ----------- 基于mmap读 ---------------
	with memory_map(filename,access=mmap.ACCESS_READ) as mp:
		print(mp.read())
	
	# ----------- 基于mmap拷贝，但不写会原区块 ---------------
	with memory_map(filename,access=mmap.ACCESS_COPY) as mp:
		mp[:3] = b'HEL'
		mp.flush()
	
	with memory_map(filename) as mp:
		v = memoryview(mp).cast('b')
		v[0]= 7
		print(mp[0:4])
		

def test_view():
	filename = 'nu.txt'
	with memory_map(filename) as mp:
		v1 = memoryview(mp)
		v =v1.cast('b')
		v[0]= 7
		print(mp[0:4]) # b'\x07ell'
		print(v[0]) # 7
		del v  # 关闭 mp 之前，必须关闭相应的视图指针 v v1
		del v1
		mp.close()
		

if __name__=="__main__":
	try:
		# test_memory_map()
		
		# test_write()
		
		test_view()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)





