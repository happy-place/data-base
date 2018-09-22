#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/23'
Info:
        
"""
import os,traceback,sys,array,io

def wirte_when_not_exists():
	'''
	只有在文件不存在时才会写出，否则抛异常，对于二进制使用 xb
	:return:
	'''
	# with open('num1.txt','xt') as f:
	# 	f.write('hahah\n')
	
	# with open('num1.txt','xt') as f: # FileExistsError: [Errno 17] File exists: 'num1.txt'
	# 	f.write('hahah\n')
	
	# 如果不存在，则写出，否则停止，防止被覆盖
	if os.path.exists('num1.txt'):
		print('{file} aleary existed.'.format(file='num1.txt'))
	else:
		with open('num1.txt','xt') as f: # FileExistsError: [Errno 17] File exists: 'num1.txt'
			f.write('hahah\n')


# 通过 io.StringIO,io.ByteIO 可以模拟真实的文件对象，并作为入参传入对应函数，实现函数测试，但对应需要真正系统文件 或管道，套接字的场合慎用
def test_stringio():
	'''
	StringIO 只能处理字符串
	:return:
	'''
	s = io.StringIO() # 创建文件对象
	s.write('hello world\n') # 第一次写入
	print('tets: ',file=s) # 第二次写入
	print(s.getvalue()) # 第一次读取
	'''
	hello world
	tets:
	'''
	s = io.StringIO("hhaha")
	print(s.read(4)) # hhah 读取4个字符
	print(s.read()) # a # 读取剩余字符
	
	
def test_byteio():
	# 操作二进制使用byteio
	s = io.BytesIO()
	s.write(b'binary data')
	print(s.getvalue()) # b'binary data'




def test_array():
	'''
	python 有提供一个array模块，用于提供基本数字，字符类型的数组。用于容纳字符号，整型，浮点等基本类型。这种模块主要用于二进制上的缓冲区，流的操作。
	二进制     还有一个鲜为人知的特性就是数组和   结构体类型能直接被写入，而 不需要中间转换为自己对象。
	Type code	C Type	Python Type	Minimum size in bytes	Notes
	'b'	signed char	int	1
	'B'	unsigned char	int	1
	'u'	Py_UNICODE	Unicode character	2	(1)
	'h'	signed short	int	2
	'H'	unsigned short	int	2
	'i'	signed int	int	2
	'I'	unsigned int	int	2
	'l'	signed long	int	4
	'L'	unsigned long	int	4
	'q'	signed long long	int	8	(2)
	'Q'	unsigned long long	int	8	(2)
	'f'	float	float	4
	'd'	double	float	8
	
	:return:
	'''
	'''
	这个适用于任何实现了被称之为”缓冲接口”的对象，这种对象会直接暴露其底层 的内存缓冲区给能处理它的操作。二进制数据的写入就是这类操作之一。
	'''
	nums = array.array('i',[1,2,3,4])
	with open('array.txt','wb') as f:
		f.write(nums)
	
	'''
	很多对象还允许通过使用文件对象的方法直接读取二进制数据到其底 层的内存中去。比如:
	'''
	a = array.array('I',[0,0,0,0])
	with open('array.txt','rb') as f:
		f.readinto(a)
	print(a) # array('i', [1, 2, 3, 4])

def test_read():
	# 逐字符读取 rt 以 text mode 读取
	with open('num.txt','rt') as f:
		while True:
			data =  f.read()
			if len(data)!=0:
				print(data,end='')
			else:
				break
	# 逐行读取
	with open('num.txt','rt') as f:
		for line in f:
			print(line,end='')
			print(line)

def test_write():
	# 如果文件已经存在，会自动覆盖 wt 以text mode 写入，at 以text mode 追加
	with open('write1.txt','wt') as f:
		f.write('hello ')
		f.write('world\n')

	# 通过print 重定向输出到文件，注只有 text mode 才允许重定向输出，二进制会失败
	with open('write2.txt','wt') as f:
		print('hello1 ',file=f,end='')
		print('world1\n',file=f)

	with open('write2.txt','at') as f:
		f.write('hello wotld')


def test_encoding():
	# 获取系统默认字符编码
	print(sys.getdefaultencoding())
	# 输出指定字符编码的字符串消息
	# with 语句会自动关闭文件，即便在有异常情况下，也是如此
	with open('write3.txt','wt',encoding='latin-1') as f:
		f.write('hello world')

def test_newline():
	# 换行符与系统有关：win - \n, unix - \r\n, open函数打开一个文件，会自动按当前系统的默认换行符，替换需要读取会写出的字符的换行符
	with open('num.txt','rt') as f:
		data = f.read()
		print(data)
	
	# 通过 newline='' 强制关闭换行符词典,会以原本形式展示换行符
	with open('num.txt','rt',newline='') as f:
		data = f.read()
		print(data)
		
def test_error():
	# 无法被解析的字段直接替换 errors='replace'
	with open('error.txt','rt',encoding='ascii',errors='replace') as f:
		print(f.read()) # Spicy Jalapen��o
	
	# 无法被解析的字段直接跳过 errors='ignore'
	with open('error.txt','rt',encoding='ascii',errors='ignore') as f:
		print(f.read()) # Spicy Jalapeno


def test_print():
	print('ACME',50,91,5) # ACME 50 91 5 空格分割
	print('ACME',50,91,5,sep=',') # ACME,50,91,5 逗号分割
	print('ACME',50,91,5,sep=',',end='!!\n') # ACME,50,91,5!! 逗号分割，!!\n 结尾
	
	for i in range(4):
		print(i) # 默认换行打印
	'''
	0
	1
	2
	3
	'''
	
	print('------')
	for i in range(4):
		print(i,end=' ') # 不换行
	print('\n------')
	'''
	------
	0 1 2 3
	------
	'''

def test_join():
	l1 = ['a',1,2]
	# print(','.join(l1)) # join 只有 str 类型list 才能使用
	print(','.join(str(x) for x in l1))
	print(*l1,sep=',')
	'''
	a,1,2
	a,1,2
	'''

def test_byte():
	# 'r','a','w' 默认为text mode
	# 读取字节型字符串
	with open('byte.txt','rb') as f:
		data = f.read()
		print(data) # b'hello world'
		print('-----')
		for d in data:
			print(d,sep=',',end='\t')
		print('\n-----')
		'''
		-----
		104	101	108	108	111	32	119	111	114	108	100
		-----
		'''
	
		for d in data.decode('utf-8'): # 字节型字符数组 转换为字符数组
			print(d,sep=',',end='\t')
		print('\n-----')
		'''
		h	e	l	l	o	 	w	o	r	l	d
		'''

	# 将字节型字符串蟹醋
	with open('byte.txt','wb') as f:
		f.write(b'hello world')
		f.write('hello world'.encode('utf-8')) # 字符按utf8编码
	
	


	
if __name__=="__main__":
	try:
		# test_read()
		# test_write()
		# test_encoding()
		# test_newline()
		# test_error()
		# test_print()
		# test_join()
		# test_byte()
		
		# test_array()
		
		# wirte_when_not_exists()
		
		# test_stringio()
		
		test_byteio()
		
		# print(str(b'hello world',encoding='latin'))
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)









