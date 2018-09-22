#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""

import os,traceback,fnmatch,gzip,bz2,re

# 第一层迭代器，遍历给定目录下文件，查找相匹配的文件绝对路径构成的集合，转换为迭代器返回
def gen_find(filepat,top):
	'''
	遍历顶层目录，构建复合匹配模式的文件树
	:param filepat:
	:param top:
	:return:
	'''
	for path,dirlist,filelist in os.walk(top): # 当前路径，当前路径下目录清单，当前路径下文件名单
		for name in fnmatch.filter(filelist,filepat): # 只对文件进行匹配过滤
			yield os.path.join(path,name) # 拼接复合匹配逻辑的文件路径返回

# 第二层迭代器：封装第一层匹配的文件的打开文件流 (文件句柄)
def gen_opener(filenames):
	for filename in filenames:
		if filename.endswith('.gz'):
			f = gzip.open(filename,'rt')
		elif filename.endswith('.bz2'):
			f = bz2.open(filename,'bz2')
		else:
			f = open(filename,'rt')
		yield f
		f.close() # 迭代器调用接受会自行关闭每一个文件

# 第三层迭代器：封装文件流中读取的每行内容
def gen_concatenate(iterations):
	'''
	将文件迭代器进一步封装到迭代器中
	:param iterations:
	:return:
	'''
	for it in iterations:
		yield from it

# 第四层迭代器：封装封装匹配的内容字符
def gen_grep(pattern,lines):
	pat = re.compile(pattern)
	for line in lines:
		if pat.search(line):
			yield line
	
def test_pipe():
	lognames = gen_find('access-logs*','/Users/huhao/Desktop/aa')
	files = gen_opener(lognames)
	lines = gen_concatenate(files)
	matchlines = gen_grep('(?i)select',lines)
	for line in matchlines:
		print(line)
	
	# 统计总共抓取字节数
	bytecolumn = (len(line) for line in matchlines)
	bytes = (int(x) for x in bytecolumn if x !='-')
	print("total bytes: {bytes}".format(bytes=sum(bytes))) # total bytes: 11052

if __name__=="__main__":
	try:
		# test_pipe()
		
		# print(' aa bb cc '.rsplit(None,1))
		
		test_pipe()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




