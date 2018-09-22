#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/26'
Info:
        
"""
import os,traceback,sys
import struct,itertools
from struct import Struct
from collections import namedtuple


# if sys.version_info[0]==2:
# 	import numpy as np
# else:
# 	print('module numpy need python2.x!')
# 	exit(0)


def write_records(records,format,f):
	record_struct = Struct(format)
	for r in records:
		f.write(record_struct.pack(*r))
		
		
def save_records():
	records = [ (1, 2.3, 4.5),
	            (6, 7.8, 9.0),
	            (12, 13.4, 56.7) ]
	with open('data.b','wb') as f:
		write_records(records,'<idd',f)
	'''
	结构体通常会使用一些结构码值i, d, f等 [参考 Python文档 ]。 这些代码分别代表某个特定的二进制数据类型如32位整数，64位浮点数，
	32位浮点数等。 第一个字符 < 指定了字节顺序。在这个例子中，它表示”低位在前”。 更改这个字符为 > 表示高位在前，或者是 ! 表示网络字节顺序。
	'''
		
		
def unpack_records(format,data):
	record_struct = Struct(format)
	return (record_struct.unpack_from(data,offset) for offset in range(0,len(data), record_struct.size))


def read_records():
	with open('data.b','rb') as f:
		data = f.read()

	recs = unpack_records('<idd',data)
	print(type(recs))
	
	l1 = list(recs) # <class 'generator'>
	print(l1[0])
	
	for rec in l1:
		print(rec)

def fast_strcut():
	record_struct = Struct('<idd')
	print(record_struct.size) # 结构体包含字节数 20
	
	bin = record_struct.pack(1,2.0,3.0) # b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@'
	print(bin) # (1, 2.0, 3.0)
	
	data = record_struct.unpack(bin)
	print(data) # 解码
	

def test_struct():
	# struct 模块级别调用
	bin = struct.pack('<idd',1,2.0,3.0)
	print(bin) # b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@'
	
	data = struct.unpack_from('<idd',bin)
	print(data) # (1, 2.0, 3.0)
	
def unpack_records(format,data):
	record_struct = Struct(format)
	return (record_struct.unpack(data[offset:offset + record_struct.size]) for offset in range(0,len(data),
	                                                                                 record_struct.size))


def read_records1(format,f):
	record_struct = Struct(format)
	chunks = iter(lambda:f.read(record_struct.size),b'')
	return (record_struct.unpack(chunk) for chunk in chunks)


	
def test_iter():
	# 通过迭代去读取二进制文件
	# with open('data.b','rb') as f:
	# 	chunks = iter(lambda: f.read(20),b'')
	# 	for chk in chunks:
	# 		print(chk)
	# 	'''
	# 	b'\x01\x00\x00\x00ffffff\x02@\x00\x00\x00\x00\x00\x00\x12@'
	# 	b'\x06\x00\x00\x00333333\x1f@\x00\x00\x00\x00\x00\x00"@'
	# 	b'\x0c\x00\x00\x00\xcd\xcc\xcc\xcc\xcc\xcc*@\x9a\x99\x99\x99\x99YL@'
	# 	'''
	
	# with open('data.b','rb') as f:
	# 	record_struct = Struct('<idd')
	# 	chunks = iter(lambda: f.read(record_struct.size),b'')
	#
	# 	for chk in chunks:
	# 		rec = record_struct.unpack_from(chk)
	# 		# rec = record_struct.unpack(chk)
	# 		print(rec)
	#
	# 	'''
	# 	(1, 2.3, 4.5)
	# 	(6, 7.8, 9.0)
	# 	(12, 13.4, 56.7)
	# 	在函数 unpack_records() 中使用了另外一种方法 unpack_from() 。 unpack_from() 对于从一个大型二进制数组中提取二进制数据非常有用，
	# 	 因为它不会产生任何的临时对象或者进行内存复制操作。 你只需要给它一个字节字符串(或数组)和一个字节偏移量，它会从那个位置开始直接解包数据。
	# 	'''
	
	with open('data.b','rb') as f:
		chunks = iter(lambda: f.read(20),b'')
		for chk in chunks:
			rec = unpack_records('<idd',chk)
			print(list(rec)[0])
				
	
def unpack_by_nametuple():
	Record = namedtuple('Record',['kind','x','y'])
	# 结合 nametuple 和 结构体，提取二进制数据
	with open('data.b','rb') as f:
		records = (Record(*r) for r in read_records1('<idd',f))
		
		for r in records:
			print(r.kind,r.x,r.y)
		
		'''
		1 2.3 4.5
		6 7.8 9.0
		12 13.4 56.7
		'''

# def use_numpy():
# 	'''
# 	大批量二进制数据有限考虑通过 numpy 读取
# 	，如果你需要从已知的文件格式(如图片格式，图形文件，HDF5等)中读取二进制数据时， 先检查看看Python是不是已经提供了现存的模块
# 	:return:
# 	'''
# 	with open('data.b','rb') as f:
# 		records = np.fromfile(f,dtype = '<i,<d,<d')
# 		print(records)
# 		print(records[0])
# 		print(records[1])
	
# -------------- 方案1：直接变解码 --------------------
def write_polys(filename,polys):
	# 串接多个list
	flattened  = list(itertools.chain(*polys))
	min_x = min(x for x,y in flattened)
	max_x = max(x for x,y in flattened)
	min_y = min(y for x,y in flattened)
	max_y = max(y for x,y in flattened)
	'''
	+------+--------+------------------------------------+
	|Byte  | Type   |  Description                      |
	+======+========+====================================+
	|0     | int    |  文件代码（0x1234，小端）            |
	+------+--------+------------------------------------+
	|4     | double |  x 的最小值（小端）                  |
	+------+--------+------------------------------------+
	|12    | double |  y 的最小值（小端）                  |
	+------+--------+------------------------------------+
	|20    | double |  x 的最大值（小端）                  |
	+------+--------+------------------------------------+
	|28    | double |  y 的最大值（小端）                  |
	+------+--------+------------------------------------+
	|36    | int    |  三角形数量（小端）                   |
	+------+--------+------------------------------------+
	'''

	with open(filename,'wb') as f:
		# step1: 按如些格式编码文件头，记录了文件代码，全部多边形中x,y的极值，以及总共多边形数  << 编码文件的元数据
		f.write(struct.pack('<iddddi',0x1234,min_x,min_y,max_x,max_y,len(polys)))
		'''
		+------+--------+------------------------------------+
		|Byte  | Type   |  Description                      |
		+======+========+====================================+
		|0     | int    |  文件代码（0x1234，小端）            |
		+------+--------+------------------------------------+
		|4     | double |  x 的最小值（小端）                  |
		+------+--------+------------------------------------+
		|12    | double |  y 的最小值（小端）                  |
		+------+--------+------------------------------------+
		|20    | double |  x 的最大值（小端）                  |
		+------+--------+------------------------------------+
		|28    | double |  y 的最大值（小端）                  |
		+------+--------+------------------------------------+
		|36    | int    |  三角形数量（小端）                   |
		+------+--------+------------------------------------+
		'''
		
		for poly in polys: # 遍历全部多边形
			size = len(poly) * struct.calcsize('<dd') # 当前多边形的点数 x 记录每个点小的字节数 = 记录当前多边形需要的字节数 (存储点集合需要的空间)
			f.write(struct.pack('<i',size+4)) # 在记录当前多边形需要的字节数基础上 + 一个 int(存储点集合需要空间的元数据需要的空间)，点空间size + 记录空间4
			for pt in poly:
				f.write(struct.pack('<dd',*pt)) # 轮询存储当前多边形的每一个带你
			'''
			+------+--------+-------------------------------------------+
			|Byte  | Type   |  Description                              |
			+======+========+===========================================+
			|0     | int    |  记录长度（N字节）                          |  int = 4bytes
			+------+--------+-------------------------------------------+
			|4+N   | Points |  (X,Y) 坐标，以浮点数表示                   |
			+------+--------+-------------------------------------------+
			'''
	

def read_polys(filename):
	with open(filename,'rb') as f:
		# step1：读取编码，极值，多边形总数
		header = f.read(40)
		file_code,min_x,min_y,max_x,max_y,num_polys = struct.unpack('<iddddi',header) # 4 + 8*4 + 4 = 40bytes
		polys = []
		for n in range(num_polys):
			pbytes, =struct.unpack('<i',f.read(4)) # 读取每个多边形总点数
			poly = []
			for m in range(pbytes // 16): # 每个点由(double,double)组成double=8bytes 轮询读取当前多边形的每一个点
				pt = struct.unpack('<dd',f.read(16))
				poly.append(pt) # 将解析出点，填充到当前多边形
			polys.append(poly) # 将解析出的多边形，填充到多边形集合
	return polys


def test_write_polys():
	polys = [
		[ (1.0, 2.5), (3.5, 4.0), (2.5, 1.5) ],
		[ (7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0) ],
		[ (3.4, 6.3), (1.2, 0.5), (4.6, 9.2) ],
		]
	write_polys('ploys.data',polys)


def test_read_polys():
	ploys = read_polys('ploys.data')
	print(ploys)
	'''
	[[(1.0, 2.5), (3.5, 4.0), (2.5, 1.5)], [(7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0)], [(3.4, 6.3), (1.2, 0.5), (4.6, 9.2)]]
	'''

# -------------- 方案2：借助类封装结构体 --------------------
class StructField:
	def __init__(self,format,offset):
		self.format = format
		self.offset = offset
		
	def __get__(self,instance,cls):
		if instance is None:
			return self
		else:
			r = struct.unpack_from(self.format,instance._buffer,self.offset)
			return r[0] if len(r) ==1 else r # 如果只有一个元素就解封
		
class Structure:
	def __init__(self,bytedata):
		self._buffer = memoryview(bytedata)
		
class PolyHeader(Structure):
	file_code = StructField('<i',0)  # 从offset = 0 位置开始读，读取 int = 4bytes
	min_x = StructField('<d',4) # 从offset = 4 位置开始读，读取 double = 8bytes
	min_y = StructField('<d',12)
	max_x = StructField('<d',20)
	max_y = StructField('<d',28)
	num_polys = StructField('<d',36)


def test_read_by_class():
	# 读取 ploys.data 文件的首行元数据
	with open('ploys.data','rb') as f:
		phead = PolyHeader(f.read(40))
		print(phead.file_code == 0x1234)
		print(phead.min_x,phead.min_y,phead.max_x,phead.max_y,phead.num_polys)

# -------------- 方案3：借助反射自动解析 --------------------

class StructureMeta(type):
	def __init__(self,clsname,bases,clsdict):
		fields = getattr(self,'_fields_',[])
		byte_order = ''
		offset = 0
		for format,fieldname in fields:
			if format.startswith(('<','>','!','@')):
				byte_order = format[0]
				format = format[1:]
			format = byte_order + format
			setattr(self,fieldname,StructField(format,offset))
			offset += struct.calcsize(format)
		setattr(self,'struct_size',offset)

class Structure1(metaclass=StructureMeta):
	def __init__(self,bytedata):
		self._buffer = bytedata
	
	@classmethod
	def from_file(cls,f):
		return cls(f.read(cls.struct_size))
	
class PolyHeader1(Structure1):
	# 构建属性字典
	_fields_ = [
		('<i','file_code'),
		('d','min_x'),
		('d','min_y'),
		('d','max_x'),
		('d','max_y'),
		('i','num_polys'),
		]
		
def test_read_by_reflect():
	with open('ploys.data','rb') as f:
		phead = PolyHeader1.from_file(f)
		# 子类继承父类的 from_file函数，PolyHeader1 类加载时，调用了元类 StructureMeta 并类的初始化，解析 PolyHeader1 的 _fields_ ，封装成
		# Structure1 的 6个 StructField 属性抛出，然后进行遍历
		'''
		f -> PolyHeader1(Structure1(StructureMeta)) -> 通过反射提取 _fields_ 并进行遍历，将头部信息的每一条封装成 StructField 抛出
		然后基于结构体进行解析
		'''
		print(phead.file_code==0x1234)
		print(phead.min_x)
		print(phead.min_y)
		print(phead.max_x)
		print(phead.max_y)
		print(phead.num_polys)






if __name__=="__main__":
	try:
		# save_records() # python obj -> 结构体二进制编码 -> data.b
		# read_records() # data.b -> 结构体二进制解码 -> python obj
		# fast_strcut()
		# test_struct()
		
		# test_iter()
		# unpack_by_nametuple()
		# use_numpy()
		
		# test_write_polys()
		# test_read_polys()
		# test_read_by_reflect()
		
		test_sizerecord()
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)





