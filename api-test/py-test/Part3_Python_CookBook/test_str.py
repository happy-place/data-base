#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/19'
Info:
        
"""


import os,traceback,re,sys,string
from calendar import month_abbr
from collections import namedtuple

import textwrap


def test_text():
	text = 'yeah, but no, but yeah, but no, but yeah'
	print(text.startswith('yeah'))
	print(text.startswith('no'))
	print(text.find('no')) # 第10个字符出现 no
	print(text.rfind('no')) # 从左往右数 第28个字符为最右匹配项

def split_by_re():
	text1 = '11/27/2012'
	text2 = 'Nov 27, 2012'
	
	# 判断是否匹配，注 text1 = '11/27/2012a' 依然能够被匹配上 1/27/a2012 不能被匹配
	if re.match(r'\d+/\d+/\d+',text1):
		print('matched')
	else:
		print("not matched")
	
	# 打包拆分
	data = re.findall(r'(\d+)/(\d+)/(\d+)',text1)
	if data:
		day,month,year = data[0]
		print(day,month,year)
	else:
		print("not matched")

def multi_match():
	text1 = '11/27/2012'
	# 匹配模式将被多次使用时，可先编译保存,等效于 re.compile('(\\d+)/(\\d+)/(\\d+)')
	datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
	datepat = re.compile('(\\d+)/(\\d+)/(\\d+)')
	
	if datepat.match(text1):
		print("matched")
	else:
		print("not matched")
	
	data = datepat.findall(text1) # [(11,23,2012)]
	if data:
		day,month,year = data[0]
		print(day,month,year)
	else:
		print("not matched")
	
	for m in datepat.finditer(text1):  # [(11,23,2012)]
		print(m.groups())
	
	
	m = datepat.match('11/27/2013abcd')
	print(m.groups()) # ('11', '27', '2013') groups 会按匹配模式进行解封
	print(m.group()) # 11/27/2013 group 只会显示匹配区段，不会解封
	
	# 成功匹配多份
	text = '12/12/2018,11/12/2018'
	data = datepat.findall(text) # [('12', '12', '2018'), ('11', '12', '2018')]
	print(data)

	# 以(\d+)/(\d+)/(\d+) 结尾
	pattern = re.compile(r'(\d+)/(\d+)/(\d+)$')
	print(pattern.match('12/12/2012')) # <_sre.SRE_Match object; span=(0, 10), match='12/12/2012'>
	print(pattern.match('12/12/2012a')) # None


def do_replace():
	text = 'yeah, but no, but yeah, but no, but yeah'
	replace_text = text.replace('yeah', 'yep')
	print(replace_text) # yep, but no, but yep, but no, but yep 替换

def use_more():
	'''
	re.sub 对原字符串 按 年-月-日 顺序进行翻转
	
	:return:
	'''
	text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
	changed_text = re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',text) # \1 \2 \3 按序引用前面成功匹配的 (\d+)
	print(changed_text) # Today is 2012-11-27. PyCon starts 2013-3-13.
	
	# 匹配模式将被多次使用时，可将匹配模板先定下来，然后复用即可 《《《
	datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
	changed_text = datepat.sub(r'\3-\1-\2',text)
	print(changed_text) # Today is 2012-11-27. PyCon starts 2013-3-13.
	
	# 复杂逻辑匹配，可以传入转换函数解决 《《《
	data = datepat.sub(change_month,text) # Today is 27 Nov 2012. PyCon starts 13 Mar 2013.
	print(data)


def change_month(m):
	#datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
	#text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
	mon_name = month_abbr[int(m.group(1))] # 数字月转换成为英文缩写
	return '{day} {month} {year}'.format(day=m.group(2),month=mon_name,year=m.group(3))
	# Today is 27 Nov 2012. PyCon starts 13 Mar 2013.
	
	
def multi_match():
	datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
	text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
	
	organized_text,cnt = datepat.subn(r'\3-\1-\2',text)
	print(organized_text,cnt) # Today is 2012-11-27. PyCon starts 2013-3-13. 2 匹配次数

def ignore_case():
	text = 'UPPER PYTHON, lower python, Mixed Python'
	data = re.findall('python',text,flags=re.IGNORECASE)
	print(data) # ['PYTHON', 'python', 'Python']
	
	# 忽略大小写，统计将python 替换成为 snake
	data = re.sub('python','snake',text,flags=re.IGNORECASE)
	print(data) # UPPER snake, lower snake, Mixed snake


# 闭包函数
def matchcase(word):
	def replace(m):
		text = m.group()
		if text.isupper():
			return word.upper()
		elif text.islower():
			return word.lower()
		elif text[0].isupper():
			return word.capitalize()
		else:
			return word
	return replace

def shortest_match():
	str_pat = re.compile(r'\"(.*)\"')
	text1 = 'Computer says "no."'
	data = str_pat.findall(text1)
	print(data) # ['no.']
	
	text2 = 'Computer says "no." Phone says "yes."'
	data = str_pat.findall(text2)
	print(data) # ['no." Phone says "yes.'] 默认最长匹配
	
	str_pat2 = re.compile(r'\"(.*?)\"') # 添加 ? 最短匹配
	data = str_pat2.findall(text2)
	print(data) # ['no.', 'yes.']
	
def multi_line_match():
	comment = re.compile(r'/\*(.*?)\*/')
	text1 = '/* this is a comment */'
	text2 = '''/* this is a
	multiline comment */
	'''
	data = comment.findall(text1)
	print(data) # [' this is a comment ']
	
	data = comment.findall(text2)
	print(data) # []
	
	comment = re.compile(r'/\*(.*?)\*/',re.DOTALL)
	data = comment.findall(text2)
	print(data) # [' this is a\n\tmultiline comment ']

def test_join():
	parts = ['Is','Chicago','Not','Chicago?']
	print(' '.join(parts)) # 空格连接
	print(','.join(parts)) # , 连接
	print(''.join(parts))  # 直接拼接
	
	a = 'Is Chicago'
	b = 'Not Chicago?'
	
	print(a+' '+b) # Is Chicago Not Chicago?
	
	print('{} {}'.format(a,b))
	print('{} {}'.format(a,b))

def test_generator():
	data = ['ACME',50,91.1]
	print(','.join(str(d) for d in data)) # 通过生成器凭借字段

def test_print():
	a = '1'
	b = 'a'
	c = 's'
	# 只能处理 str
	print(a+':'+b+":"+c) # 1:a:s
	# print(':'.join([a,b,c])) # 1:a:s
	print(a,b,c,sep=':') # 1:a:s
	
def test_write():
	a = 'a b c'
	b = 'aa bb cc'
	
	# 只发生一次IO ，数据量小的情况下，比较合适
	with open('write1.txt' ,'w') as f:
		f.write(a+b)
		f.close()
	
	# 数据量大的情况下，先拼接会占用比较大内存，分开落盘比较合适
	with open('write2.txt' ,'w') as f:
		f.write(a)
		f.write(b)
		f.close()

# yield 所在的函数就是生成器
def sample():
	yield 'Is'
	yield 'Chicago'
	yield 'Not'
	yield 'Chicago?'

def combine(source,maxsize):
	parts = []
	size = 0
	for part in source:
		parts.append(part)
		size += len(part)
		if size > maxsize:
			yield ''.join(parts)
			parts = []
			size = 0
		yield ''.join(parts)


class People:
	def __init__(self,name,n):
		self.name = name
		self.n = n

def test_fill():
	s = '{name} has {n} messages.'
	print(s.format(name='Guid',n =37)) # Guid has 37 messages.
	name = 'Guid'
	n = 37
	print(s.format_map(vars())) # Guid has 37 messages.
	
	p = People('Guide',38)
	print(s.format_map(vars(p))) # Guide has 38 messages.

class safesub(dict):
	def __missing__(self,key):
		return '{' + key +'}'

def test_fill2():
	'''
	format 与 format_map 在 {var} 字段缺失情况下，会报错
	在对象中定义__missing__ 函数可以防止，字段缺失异常
	:return:
	'''
	s = '{name} has {n} messages.'
	name = 'Guid'
	n = 37
	del n
	print(s.format_map(safesub(vars())))

def sub(text):
	'''
	显示调用函数栈
	sub() 函数使用 sys._getframe(1) 返回调用者的栈帧。可以从中访问属性 f_locals 来获得局部变量。
	:param text:
	:return:
	'''
	return text.format_map(safesub(sys._getframe(1).f_locals))
	
def sub1():
	name = 'Guido'
	n = 27
	print(sub('Hello {name}')) # Hello Guido
	print(sub('You have {n} messages.')) # You have 27 messages.
	print(sub('Your favorite color is {color}')) # Your favorite color is {color}

	print('{name} has {n} messages.'.format_map(vars())) # Guido has 27 messages.
	
	s = string.Template('$name has $n messages.') # Guido has 27 messages.
	print(s.substitute(vars()))
	
	
def test_textwrap():
	s = '''Look into my eyes, look into my eyes, the eyes, the eyes, the eyes, not around the eyes, don't look around the eyes, look into my eyes, you're under.'''
	print(textwrap.fill(s,50)) # 将长字符串以50个字符间距切割打印输出
	print(textwrap.fill(s,40,initial_indent='  ')) # 首行缩进
	'''
	  Look into my eyes, look into my eyes,
	the eyes, the eyes, the eyes, not around
	the eyes, don't look around the eyes,
	look into my eyes, you're under.
	
	'''
	
	print(textwrap.fill(s,40,subsequent_indent='  ')) # 首行出露
	'''
	Look into my eyes, look into my eyes,
        the eyes, the eyes, the eyes, not
        around the eyes, don't look around the
        eyes, look into my eyes, you're under.
	
	'''
	
	print(os.get_terminal_size()) # 80 获取终端尺寸
	
	
if __name__=="__main__":
	try:
		# test_text()
		# split_by_re()
		# multi_match()
		# do_replace()
		# use_more()
		# multi_match()
		# ignore_case()
		
		# 保持大小写格式
		# text = 'UPPER PYTHON, lower python, Mixed Python'
		
		# data = re.sub('python',matchcase('snake'),text,flags=re.IGNORECASE)
		# print(data) # UPPER SNAKE, lower snake, Mixed Snake
		
		# shortest_match()
		
		# multi_line_match()
		
		# test_join()
		
		# test_generator()
		
		# test_print()
		
		# test_write()
		
		# print(' '.join(sample()))
		#
		# with open('write3.txt','w') as f:
		# 	for x in sample():
		# 		f.write(x)
		# 	f.close()
		
		# with open('write3.txt','w') as f:
		# 	for part in combine(sample(),32):
		# 		f.write(part)
	
		# test_fill()
		
		# test_fill2()
		
		# sub1()
		
		test_textwrap()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)






