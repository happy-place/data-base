#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/24'
Info:
        
"""

import os,traceback,time,glob,sys,io
import urllib.request
from fnmatch import fnmatch

def test_path():
	'''
	对于任何的文件名的操作，你都应该使用 os.path 模块，而不是使用标准字符串 操作来构造自己的代码。特别是为了可移植性考虑的时候更应如此，
	因为os.path模 块知道 unix 和 windows 系统之间的差异并且能够可靠地处理类似 /aa/bb/1.txt 和 \aa\bb\1.txt 这样的文件名。
	其次，你真的不应该浪费时间去重复造轮子。通常最好 是直接使用已经为你准备好的功能。
	
	:return:
	'''
	path = './test_ordereddict.py'
	path = os.path.abspath(path) # 绝对路径
	print(os.path.basename(path)) # test_ordereddict.py 文件名
	print(os.path.dirname(path)) # /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook 目录
	print(os.path.join('/aa','bb',os.path.basename(path))) # /aa/bb/test_ordereddict.py
	
	path = '~/Desktop/1.xlsx'
	print(os.path.expanduser(path)) # ~ 替代成当前用户 /Users/huhao/Desktop/1.xlsx
	print(os.path.splitext(path)) # ('~/Desktop/1', '.xlsx ') 拆分成为 路径 + 名称
	
	print(os._exists('~/Desktop/2.xlsx')) # False 是否存在
	print(os.path.isfile('/Users/huhao/Desktop/1.xlsx')) # True 是否是文件，不支持 ~ ，且文件不存在，也会返回 False
	print(os.path.isfile('test_mmap.py')) # 是否是文件，只能是 True
	
	print(os.path.isdir('/Users/huhao/Desktop')) # True 判断是否是文件目录
	print(os.path.isdir('./')) # True
	
	print(os.path.islink('test_multidict.py')) # False 判断是否是 链接文件
	print(os.path.realpath('test_multidict.py')) # 获取绝对路径 /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/test_multidict.py

	print(os.path.getsize('test_multidict.py')) # 获取文件字节数 1541
	print(os.path.getmtime('test_multidict.py')) # 获取文件字节数 1531905726.0
	print(time.ctime(os.path.getmtime('test_multidict.py'))) # 获取文件字节数 Wed Jul 18 17:22:06 2018
	print(os.stat('test_multidict.py')) # 获取详细元数据信息 os.stat_result(st_mode=33188, st_ino=14673093, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1541, st_atime=1531905726, st_mtime=1531905726, st_ctime=1531905726)
	
	print(os.listdir('./')) # 列举当前目录文件['array.txt', 'byte.txt', 'error.txt', 'merged.txt', 'merged2.txt', 'nu.txt', 'num.txt.bz2', 'num.txt.gz', 'num1.txt', 'parser.out', 'parsetab.py', 'Part3_Python_CookBook.iml', 'template.py', 'test.txt', 'test_attrgetter.py', 'test_bytearr.py', 'test_chainmap.py', 'test_complex.py', 'test_counter.py', 'test_datapressing_pipe.py', 'test_dedupe.py', 'test_deque.py', 'test_dict.py', 'test_filter.py', 'test_flatten.py', 'test_float.py', 'test_fraction.py', 'test_from_bytes.py', 'test_gzip.py', 'test_heapq.py', 'test_heapq_merge.py', 'test_html.py', 'test_io.py', 'test_itemgetter.py', 'test_iteration.py', 'test_itertools.py', 'test_list.py', 'test_match.py', 'test_mmap.py', 'test_multidict.py', 'test_nan.py', 'test_numpy.py', 'test_oct.py', 'test_ordereddict.py', 'test_os.py', 'test_parser.py', 'test_ply.py', 'test_random.py', 'test_slices.py', 'test_str.py', 'test_subscriber.py', 'test_time.py', 'test_unicode.py', 'test_unpack.py', 'test_while.py', 'test_zip.py', 'write1.txt', 'write2.txt', 'write3.txt']

def test_dir():
	filenames = (f for f in os.listdir('./') if os.path.isfile(f))
	dirs = (f for f in os.listdir('./') if os.path.isdir(f))
	print(list(filenames),list(dirs))
	
	pyfiles = (f for f in os.listdir('./') if os.path.isfile(f) and f.endswith('.py'))
	print(list(pyfiles))
	
def test_golb():
	'''
	模糊匹配查找
	:return:
	'''
	pyfiles = glob.glob('/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/*.py')
	print(pyfiles)
	
def test_fnmatch():
	cur_dir = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook'
	pyfiles = (f for f in os.listdir(cur_dir) if fnmatch(f,'*.py')) # 对比指定文件是否符合给的模式
	print(list(pyfiles))

def get_meta():
	pyfiles = glob.glob('*.py')
	time_infos = [(name,os.path.getsize(name),os.path.getmtime(name)) for name in pyfiles]
	print(time_infos) #[('parsetab.py', 1993, 1532099329.0) ...
	
	meta_infos = [(name,os.stat(name)) for name in pyfiles]
	print(meta_infos) # [('parsetab.py', os.stat_result(st_mode=33188, st_ino=14783932, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1993, st_atime=1532099329, st_mtime=1532099329, st_ctime=1532099329)), ('template.py', os.stat_result(st_mode=33188, st_ino=14817837, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=242, st_atime=1532179983, st_mtime=1532179983, st_ctime=1532179983)), ('test_attrgetter.py', os.stat_result(st_mode=33277, st_ino=14688878, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=684, st_atime=1532169769, st_mtime=1531922150, st_ctime=1532136625)), ('test_bytearr.py', os.stat_result(st_mode=33188, st_ino=14784721, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1656, st_atime=1532170048, st_mtime=1532100605, st_ctime=1532100605)), ('test_chainmap.py', os.stat_result(st_mode=33188, st_ino=14698564, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1747, st_atime=1531970306, st_mtime=1531970306, st_ctime=1531970306)), ('test_complex.py', os.stat_result(st_mode=33188, st_ino=14790811, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1542, st_atime=1532139622, st_mtime=1532139622, st_ctime=1532139622)), ('test_counter.py', os.stat_result(st_mode=33188, st_ino=14687055, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1591, st_atime=1531919386, st_mtime=1531919386, st_ctime=1531919386)), ('test_datapressing_pipe.py', os.stat_result(st_mode=33188, st_ino=14816808, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=2103, st_atime=1532177478, st_mtime=1532177478, st_ctime=1532177478)), ('test_dedupe.py', os.stat_result(st_mode=33188, st_ino=14679732, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1345, st_atime=1531914124, st_mtime=1531914124, st_ctime=1531914124)), ('test_deque.py', os.stat_result(st_mode=33188, st_ino=14660171, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1752, st_atime=1531893580, st_mtime=1531893580, st_ctime=1531893580)), ('test_dict.py', os.stat_result(st_mode=33188, st_ino=14691930, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1176, st_atime=1531962987, st_mtime=1531962987, st_ctime=1531962987)), ('test_filter.py', os.stat_result(st_mode=33188, st_ino=14690861, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1561, st_atime=1531925234, st_mtime=1531925234, st_ctime=1531925234)), ('test_flatten.py', os.stat_result(st_mode=33188, st_ino=14817373, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=707, st_atime=1532179159, st_mtime=1532179159, st_ctime=1532179159)), ('test_float.py', os.stat_result(st_mode=33188, st_ino=14787291, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=2311, st_atime=1532135493, st_mtime=1532135493, st_ctime=1532135493)), ('test_fraction.py', os.stat_result(st_mode=33188, st_ino=14792590, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=750, st_atime=1532141311, st_mtime=1532141311, st_ctime=1532141311)), ('test_from_bytes.py', os.stat_result(st_mode=33188, st_ino=14789510, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=2606, st_atime=1532179674, st_mtime=1532138071, st_ctime=1532138071)), ('test_gzip.py', os.stat_result(st_mode=33188, st_ino=14901817, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=3373, st_atime=1532400298, st_mtime=1532400298, st_ctime=1532400298)), ('test_heapq.py', os.stat_result(st_mode=33188, st_ino=14661758, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=3253, st_atime=1532179674, st_mtime=1531895124, st_ctime=1531895124)), ('test_heapq_merge.py', os.stat_result(st_mode=33188, st_ino=14817753, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1017, st_atime=1532179766, st_mtime=1532179766, st_ctime=1532179766)), ('test_html.py', os.stat_result(st_mode=33188, st_ino=14736333, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=2893, st_atime=1532048267, st_mtime=1532048267, st_ctime=1532048267)), ('test_io.py', os.stat_result(st_mode=33188, st_ino=14897670, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=6249, st_atime=1532397378, st_mtime=1532397378, st_ctime=1532397378)), ('test_itemgetter.py', os.stat_result(st_mode=33188, st_ino=14689525, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1985, st_atime=1532179674, st_mtime=1531923054, st_ctime=1531923054)), ('test_iteration.py', os.stat_result(st_mode=33188, st_ino=14813045, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=9786, st_atime=1532170350, st_mtime=1532170350, st_ctime=1532170350)), ('test_itertools.py', os.stat_result(st_mode=33188, st_ino=14813824, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=2623, st_atime=1532171678, st_mtime=1532171678, st_ctime=1532171678)), ('test_list.py', os.stat_result(st_mode=33188, st_ino=14697508, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1269, st_atime=1531969051, st_mtime=1531969051, st_ctime=1531969051)), ('test_match.py', os.stat_result(st_mode=33188, st_ino=14701065, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=2914, st_atime=1531974360, st_mtime=1531974360, st_ctime=1531974360)), ('test_mmap.py', os.stat_result(st_mode=33188, st_ino=14947400, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=2031, st_atime=1532431093, st_mtime=1532431093, st_ctime=1532431093)), ('test_multidict.py', os.stat_result(st_mode=33188, st_ino=14673093, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1541, st_atime=1531905726, st_mtime=1531905726, st_ctime=1531905726)), ('test_nan.py', os.stat_result(st_mode=33188, st_ino=14791287, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=825, st_atime=1532140218, st_mtime=1532140218, st_ctime=1532140218)), ('test_numpy.py', os.stat_result(st_mode=33188, st_ino=14799021, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=4305, st_atime=1532148903, st_mtime=1532148903, st_ctime=1532148903)), ('test_oct.py', os.stat_result(st_mode=33188, st_ino=14788409, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=983, st_atime=1532136623, st_mtime=1532136623, st_ctime=1532136623)), ('test_ordereddict.py', os.stat_result(st_mode=33188, st_ino=14673529, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=856, st_atime=1531906238, st_mtime=1531906238, st_ctime=1531906238)), ('test_os.py', os.stat_result(st_mode=33188, st_ino=14952016, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=4580, st_atime=1532434018, st_mtime=1532434016, st_ctime=1532434016)), ('test_parser.py', os.stat_result(st_mode=33188, st_ino=14782941, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=3582, st_atime=1532098410, st_mtime=1532098410, st_ctime=1532098410)), ('test_ply.py', os.stat_result(st_mode=33188, st_ino=14783909, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1520, st_atime=1532099310, st_mtime=1532099310, st_ctime=1532099310)), ('test_random.py', os.stat_result(st_mode=33188, st_ino=14801699, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1522, st_atime=1532152087, st_mtime=1532152087, st_ctime=1532152087)), ('test_slices.py', os.stat_result(st_mode=33188, st_ino=14692046, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1302, st_atime=1531963164, st_mtime=1531963164, st_ctime=1531963164)), ('test_str.py', os.stat_result(st_mode=33188, st_ino=14733006, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=9271, st_atime=1532014097, st_mtime=1532014097, st_ctime=1532014097)), ('test_subscriber.py', os.stat_result(st_mode=33188, st_ino=14696308, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1763, st_atime=1531967791, st_mtime=1531967791, st_ctime=1531967791)), ('test_time.py', os.stat_result(st_mode=33188, st_ino=14807496, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=5876, st_atime=1532183016, st_mtime=1532161149, st_ctime=1532161149)), ('test_unicode.py', os.stat_result(st_mode=33188, st_ino=14726650, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=5423, st_atime=1532001878, st_mtime=1532001878, st_ctime=1532001878)), ('test_unpack.py', os.stat_result(st_mode=33188, st_ino=14653715, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1965, st_atime=1531883455, st_mtime=1531883455, st_ctime=1531883455)), ('test_while.py', os.stat_result(st_mode=33188, st_ino=14818824, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1821, st_atime=1532183047, st_mtime=1532183047, st_ctime=1532183047)), ('test_zip.py', os.stat_result(st_mode=33188, st_ino=14813661, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=4005, st_atime=1532171344, st_mtime=1532171344, st_ctime=1532171344))]
	
	
def bad_filename(filename):
	try:
		print(filename)
	except UnicodeEncodeError:
		# filename = repr(filename)[1:-1] # 'b\udce4d.txt' 文件系统要求不严格情况下，混入问题编码名称的文件时，需要特殊处理
		filename.encode(sys.getfilesystemencoding(),errors='surrogateescape')
		'''
		surrogateescape
		Python 3 中新增的 surrogateescape 则是一种可逆的错误处理机制，利用 Surrogate 码位保存无法解码的字节，编码时则将其还原为对应的原始字节。
  
		'''
		print(filename)
	finally:
		return filename

def test_errorcode():
	print(sys.getfilesystemencoding()) # utf-8 获取文件系统字符编码
	

def test_textiowrapper():
	u = urllib.request.urlopen('http://www.python.org')
	# 1.读取二进制数据
	# data = u.read()
	# print(data) # b'<!doctype html>\n<!--[if lt IE 7]>    ......
	# 2.在比关闭流情况下，通过对象包装方式修改编码，且不改版流元数据内容
	f = io.TextIOWrapper(u,encoding='utf-8')
	text = f.read()
	print(text)
	f.close()
	'''
	<!doctype html> ....
	
	'''

def test_detach():
	'''
	如果你想修改一个已经打开的文本模式的文件的编码方式，可以先使用detach()方法移除掉已存在的文本编码层，并使用新的编码方式代替。
	'''
	
	print(sys.stdout.encoding)
	sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding='latin-1')
	print(sys.stdout.encoding)


def test_io():
	with open('nu.txt','r') as f:
		print(f) # <_io.TextIOWrapper name='nu.txt' mode='r' encoding='UTF-8'> 编解码Unicode文本处理层
		print(f.buffer) # <_io.BufferedReader name='nu.txt'>处理二进制数据带缓存IO层
		print(f.buffer.raw) # <_io.FileIO name='nu.txt' mode='rb' closefd=True> 操作系统底层危机描述符的原始文件

def test_io2():
	with open('nu.txt','r') as f:
		print(f) # <_io.TextIOWrapper name='nu.txt' mode='r' encoding='UTF-8'> 编解码Unicode文本处理层
		b = f.detach() # 端口 f
		print(b) # <_io.BufferedReader name='nu.txt'>处理二进制数据带缓存IO层
		print(b.raw) # <_io.FileIO name='nu.txt' mode='rb' closefd=True> 操作系统底层危机描述符的原始文件
		# b报错 ValueError: underlying buffer has been detached
		f = io.TextIOWrapper(b,encoding='latin-1') # <_io.TextIOWrapper name='nu.txt' encoding='latin-1'> 重新包装回去
		print(f)

def test_xmlcharrefplace():
	sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding='ascii',errors='xmlcharrefreplace')
	print(b'Jalape\u00fio')

def write_bytes_to_file():
	try:
		sys.stdout.write(b'Hello\n') # 无法直接在 TextIOWrapper 层将二进制写入文件
	except:
		print('write error')
		sys.stdout.buffer.write(b'Hello\n') # 从Buffered 层将二进制写入文件是 ok的

def test_close():
	# 创建 IO 通道
	iofile = os.open('nu.txt',os.O_WRONLY|os.O_CREAT)
	# 使用文件对象包裹
	textfile = open(iofile,'wt')
	# textfile = open(iofile,'wt',closed=False) 默认高级流关闭或损坏时，低级流也会自动关闭，通过closed=False 设置，可以在高级流损坏状态下，不关闭低级流
	textfile.write('big table\n') # 通过操作文件对象完成数据刷写
	textfile.close() # 关闭高级流同时字段关闭低级流
	
	
	




if __name__=="__main__":
	try:
		# test_path()
		# test_dir()
		# test_golb()
		# test_fnmatch()
		# get_meta()
		# test_textiowrapper()
		# test_detach()
		# test_io()
		# test_io2()
		# test_xmlcharrefplace()
		# write_bytes_to_file()
		test_close()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


