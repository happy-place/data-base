#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/25'
Info:
        
"""

import os,traceback,tempfile
from tempfile import TemporaryFile,NamedTemporaryFile,TemporaryDirectory



def test_tempfile():
	with TemporaryFile('w+t') as f: # 创建临时文件 'w+' write and read , t text mode
		f.write('hello world\n') # 写出
		f.write('testing\n')
		f.seek(0) # 游标回拨
		data = f.read() # 从起始位置读取
		print(data)
		f.close() # 语句之后自动销毁
		'''
		hello world
		testing
		'''

def test_wr(filename):
	with open(filename,'w+') as f:
		f.write('hello world\n')
		f.seek(0)
		print(f.read())

def test_namedtemporaryfile():
	with NamedTemporaryFile('w+t',delete=True) as f: # 创建了临时文件，默认delete=True f.close() 调用后自动删除临时文件，False 会保留
		filename = f.name # 获取临时文件名称
		print('temporary file name is ',filename)
		test_wr(filename) # 对临时文件进行读写测试
		print(os.path.exists(filename)) #  True

	print(os.path.exists(filename)) # 测试临时文件是否存在 False

def test_temporarydir():
	with TemporaryDirectory() as dir: # 创建了零食文件名目录
		print(os.path.isdir(dir)) # True
		print(dir) # /var/folders/gc/nlxcp8p95vj4zfmq0tjz6zf80000gn/T/tmp1xfru7dj
	print(os.path.exists(dir)) # False

def test_mkstemp():
	
	try:
		tempdir = tempfile.gettempdir() # tempfile 模块创建的临时文件和临时文件夹的根路径
		print(tempdir) # /var/folders/gc/nlxcp8p95vj4zfmq0tjz6zf80000gn/T
		
		n,filename = tempfile.mkstemp() # 手动创建临时文件，创建后不会自动删除
		print(filename,os.path.isfile(filename)) # /var/folders/gc/nlxcp8p95vj4zfmq0tjz6zf80000gn/T/tmpec4cec0k True
		
		dir = tempfile.mkdtemp()  # 手动创建临时文件目录，创建后不会自动删除
		print(dir,os.path.isdir(dir)) # /var/folders/gc/nlxcp8p95vj4zfmq0tjz6zf80000gn/T/tmphu2_y8oi True
		
		# /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/aa
		with NamedTemporaryFile(prefix='temp',suffix='.txt',
		                        dir='/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/aa') as f:
			fn = f.name # /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/aa/tempr0_1bpfn.txt
			print(fn)
			# 使用完毕自动删除，
			
		if os.path.exists(fn):
			print('remove {fn}'.format(fn=fn))
			os.remove(fn)
		
		
		
		
	finally:
		os.remove(filename)
		os.removedirs(dir)
		
	# print(tempfile.mkstemp())
	# print(tempfile.mkdtemp() )
	




if __name__=="__main__":
	try:
		# test_tempfile()
		# test_namedtemporaryfile()
		# test_temporarydir()
		test_mkstemp()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)



