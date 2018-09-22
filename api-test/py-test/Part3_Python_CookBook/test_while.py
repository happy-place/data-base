#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:

"""
import os,traceback,sys

'''
iter 函数一个鲜为人知的特性是它接受一个可选的 callable 对象和一个标记 (结 尾) 值作为输入参数。当以这种方式使用的时候，它会创建一个迭代器，
这个迭代器会 不断调用 callable 对象直到返回值和标记值相等为止。
这种特殊的方法对于一些特定的会被重复调用的函数很有效果，比如涉及到 I/O 调用的函数。
举例来讲，如果你想从套接字或文件中以数据块的方式读取数据，通常 你得要不断重复的执行 read() 或 recv() ，
并在后面紧跟一个文件结尾测试来决定是 否终止。这节中的方案使用一个简单的 iter() 调用就可以将两者结合起来了。
其中 lambda 函数参数是为了创建一个无参的 callable 对象，并为 recv 或 read() 方法提 供了 size 参数。
'''


# 8k对齐
CHUNKSIZE=8192

def reader(s):
	'''
	通过while 轮询拉取文件
	:param s:
	:return:
	'''
	try:
		f = open(s,'r')
		while True:
			data = f.read(CHUNKSIZE)
			if data == '':
				break
			print(data,end='')
	finally:
		if f is not None:
			f.close()

def reader2(s):
	'''
	通过迭代器轮询拉取文
	:param s:
	:return:
	'''
	try:
		f = open(s,'r')
		for line in iter(lambda :f.read(CHUNKSIZE),''): # '' 为迭代器轮训结束标记
			sys.stdout.write(line)
	finally:
		if f is not None:
			f.close()



def test_reader():
	reader('test_time.py')



if __name__=="__main__":
	try:
		
		test_reader()
		
		
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)








