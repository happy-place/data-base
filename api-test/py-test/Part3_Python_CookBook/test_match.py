#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/19'
Info:
        
"""


import os,traceback,re
from urllib.request import urlopen
from fnmatch import fnmatch,fnmatchcase



def split_by_re():
	'''
	正则拆分
	:return:
	'''
	line = 'asdf fjdk; afed, fjek,asdf, foo hahh'
	
	# 使用中括号 [] 只会截取匹配元素
	data = re.split(r'[;,\s\t]\s*',line) # 被分号; 逗号, 空白符\s 制表符\t分割 且分隔符后有0~n个空白符
	print(data) # ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo', 'hahh']
	
	# 使用小括号() 和 |， 连带分割符，也会被收集
	data = re.split(r'(;|,|\s\t)\s*',line) # ['asdf fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo hahh']
	print(data)
	
	values = data[::2] # 提取字段
	delimiters = data[1::2] +[''] # 提取分隔符
	print(values,delimiters) # ['asdf fjdk', 'afed', 'fjek', 'asdf', 'foo hahh'] [';', ',', ',', ',', '']
	
	# 重新拼接回去，如果存在多个空格，则会损失精度
	print(''.join(v+d for v,d in zip(values,delimiters))) # asdf fjdk;afed,fjek,asdf,foo hahh
	
	
def test_match():
	filename = 'spam.txt'
	print(filename.endswith('.txt')) # 结尾
	print(filename.startswith('file')) # 开头
	
	url = 'http://www.python.org'
	print(url.startswith("http:"))
	

def filter():
	filenames = os.listdir('.')
	# 创建生成器 遍历当前目录下的文件，如果以 .py 或 .h 结尾 就收集 endswith 多值匹配使用 Tuple
	generator = (filename for filename in filenames if filename.endswith(('.py','.h')))
	print(list(generator))
	
	print(all(name.endswith('.py') for name in filenames)) # False 全部以.py 结尾
	print(any(name.endswith('.py') for name in filenames)) # True 任何一个以.py 结尾
	
def read_res(name):
	# 等效于
	if re.match('http:|https:|ftp:',name):
	# if name.startswith(('http:','https:','ftp:')):
		
		print(urlopen(name).read())
	else:
		with open(name) as f:
			lines = f.readlines()
			print(lines)
			f.close()

def test_fnmatch():
	# fnmatch 在mac os 上严格区分大小写，在windows中不区分，
	print(fnmatch('foo.txt','*.txt')) # True
	print(fnmatch('foo.txt','*.TXT')) # False
	
	# 使用fnmatchcase 强制区分大小写
	print(fnmatchcase('foo.txt','*.TXT')) # False
	
	addresses = [
		'5412 N CLARK ST',
		'1060 W ADDISON ST',
		'1039 W GRANVILLE AVE',
		'2122 N CLARK ST',
		'4802 N BROADWAY',
		]
	
	print([addr for addr in addresses if fnmatch(addr,'* ST') ]) # 以ST 结尾 ['5412 N CLARK ST', '1060 W ADDISON ST', '2122 N CLARK ST']
	print([addr for addr in addresses if fnmatch(addr,'54[0-9][0-9] *ST') ]) # ['5412 N CLARK ST']
	


if __name__=="__main__":
	try:
		# split_by_re()
		# test_match()
		# filter()
		# read_res('https://www.baidu.com') # 从网页读取
		# read_res('./test.txt') # 从文件读取
		
		test_fnmatch()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


