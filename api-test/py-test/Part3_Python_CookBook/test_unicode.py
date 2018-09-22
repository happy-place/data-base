#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/19'
Info:
        
"""

import os,traceback,re,sys
import unicodedata


def not_equals():
	s1 = 'Spicy Jalape\u00f1o'
	s2 = 'Spicy Jalapen\u0303o'
	
	print(s1,len(s1)) # Spicy Jalapeño 14 整体编码
	print(s2,len(s2)) # Spicy Jalapeño 15 拉丁分散编码
	print(s1==s2) # False
	
	# NFC 整体按一种编码走
	t1 = unicodedata.normalize('NFC',s1) # Spicy Jalapeño 14
	t2 = unicodedata.normalize('NFC',s2) # Spicy Jalapeño 14
	print(t1,len(t1))
	print(t2,len(t2))
	print(t1==t2) # True
	
	# NFC 分拆编码
	t1 = unicodedata.normalize('NFD',s1) # Spicy Jalapeño 15
	t2 = unicodedata.normalize('NFD',s2) # Spicy Jalapeño 15
	print(t1,len(t1))
	print(t2,len(t2))
	print(t1==t2) # True
	
	s = '\ufb01' # A single character
	print(s) # ﬁ
	t1 = unicodedata.normalize('NFD',s)
	print(t1) # ﬁ
	
	# Python 同样支持扩展的标准化形式 NFKC 和 NFKD，它们在处理某些字符的时 候增加了额外的兼容特性
	t1 = unicodedata.normalize('NFKD',s)
	print(t1) # fi
	
	t1 = unicodedata.normalize('NFKC',s)
	print(t1) # fi

def do_clean():
	'''
	清除变音符
	:return:
	'''
	s1 = 'Spicy Jalape\u00f1o'
	t1 = unicodedata.normalize('NFD',s1)
	print(type(t1)) # <class 'str'>
	data = ''.join(c for c in t1 if not unicodedata.combining(c)) # combining 可测试字符是否是和音字符
	print(data) # Spicy Jalapeno

def re_in_unicode():
	num = re.compile('\d+')
	if num.match('123'):
		data = num.findall('123')
		print(data) # ['123']
	
	data = num.findall('\u0661\u0662\u0663')
	
	if data:
		print(data) # ['١٢٣']
	

def match_arabic():
	'''
	混合使用 Unicode 和正则表达式通常会让你抓狂。如果你真的打算这样做的话，最 好考虑下安装第三方正则式库，
	它们会为 Unicode 的大小写转换和其他大量有趣特性 提供全面的支持，包括模糊匹配。
	:return:
	'''
	arabic = re.compile('[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+')
	pat = re.compile('stra\u00dfe', re.IGNORECASE)
	s = 'straße'
	if pat.match(s):
		print(pat.findall(s)) # ['straße'] 能够正常匹配
		print(pat.findall(s.upper())) # [] 匹配不成功
	
	
def test_strip():
	s = ' hello world \n'
	print(s.strip()) # 删收尾
	print(s.lstrip()) # 删左
	print(s.rstrip()) # 删右空白符
	
	t = '-----hello====='
	print(t.lstrip('-')) # 删 左-
	print(t.strip('-=')) # 删 右=
	
	s = ' hello world \n'
	s = s.strip()
	print(s)
	
	# print(s.replace(' ','')) # helloworld
	print(re.sub('\s+',' ',s).strip()) # hello world 使用正则删除
	
def read_file():
	with open('test.txt') as f:
		lines = (line.strip() for line in f) # 先创建生成器，使用时再加载数据
		for line in lines:
			print(line)
		f.close()
		
def do_clean():
	# 方案1： 将 \t \f 替换成为 ' ', \r 替换成为None(即删除)，然后将全部Unicode 的音符键 使用相同手段替换成为None
	s = 'pýtĥöñ\fis\tawesome\r\n'
	print(s)
	
	remap = {ord('\t'):' ',ord('\f'):' ',ord('\r'):None}
	s = s.translate(remap) # 删除全部 \r，将\t,\f 替换成为 ' '
	print(s)
	
	cmd_chr = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
	print(cmd_chr) # {768: None, 769: None, 770: None, ...} # 将全部 unicode 音符键的 value 设置为 None
	
	b = unicodedata.normalize('NFD',s) # 删除全部音符键
	print(b)
	
	s = b.translate(cmd_chr) # python is awesome
	print(s)
	
	# 方案2：先将原始输入按标准化为分解形式字符，在结合 encode() decode() 编解码操作 清楚不可识别字符
	s = 'pýtĥöñ\fis\tawesome\r\n'
	b = unicodedata.normalize('NFD',s) # 先进行整体编码
	print(b)
	
	b = b.encode('ascii','ignore').decode('ascii') # 按 ascii 进行编码，忽略不能识别的字符，然后使用ascii解码，
	print(b) # pythonis	awesome


def clean_space():
	s = 'hell\t oworld\t\f\n'
	
	# 适合数据量大替换逻辑
	s = s.replace('\t','').replace('\f','').replace('\n','').replace(' ','')
	print(s)
	
	# 正则替换 适合复杂删除逻辑
	s = 'hell\t oworld\t\f\n'
	print(re.sub('\s+','',s)) # helloworld

	# 词典替换
	replace_dict = {ord('\t'):'',ord('\n'):'',ord('\f'):'',ord(' '):''} # helloworld
	s = s.translate(replace_dict)
	print(s)

def place():
	text = 'hello world'
	print(text.ljust(20,'-'))  # hello world---------
	print(text.rjust(20,'-'))  # ---------hello world
	print(text.center(20,'-')) # ----hello world-----
	
	# format 可同时处理字符 和 数字
	print(format(text,'>20')) # '         hello world'
	print(format(text,'<20')) # 'hello world         '
	print(format(text,'^20')) # '    hello world     '
	
	print(format(text,'->20s')) # ---------hello world
	print(format(text,'-<20s')) # hello world---------
	print(format(text,'-^20s')) # ----hello world-----
	
	print("{:>10s} {:>10s}".format('hello','world')) #      hello      world
	
	x = 1.2345
	print(format(x,'>10')) # '    1.2345'
	print(format(x,'<10')) # '1.2345    '
	print(format(x,'^10.2f')) # '   1.23   '
	
	print('%-20s' % text) # 'hello world         '
	print('%20s' % text)  # '         hello world'


if __name__=="__main__":
	try:
		# not_equals()
		# do_clean()
		# re_in_unicode()
		# match_arabic()
		# test_strip()
		
		# read_file()
		# do_clean()
		
		# clean_space()
		
		place()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)











