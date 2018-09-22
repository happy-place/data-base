#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/19'
Info:
        
"""

import os,traceback,html,re
from html.parser import HTMLParser
from xml.sax.saxutils import unescape
from collections import namedtuple


def test_html():
	s = 'Elements are written as "<tag>text</tag>".'
	print(s) # Elements are written as "<tag>text</tag>".
	print(html.escape(s)) # Elements are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.
	print(html.escape(s,quote=False)) # Elements are written as "&lt;tag&gt;text&lt;/tag&gt;".
	
	# 将非ascii文本 嵌入
	s = 'Spicy Jalapeño'
	print(s.encode('ascii', errors='xmlcharrefreplace')) # b'Spicy Jalapen&#771;o'
	
	s = 'Spicy &quot;Jalape&#241;o&quot.'
	p = HTMLParser()
	print(p.unescape(s)) # Spicy "Jalapeño".
	
	t = 'The prompt is &gt;&gt;&gt;'
	print(unescape(t)) # The prompt is >>>


def generate_token(pat,text):
	# 定义Token 对象
	Token = namedtuple('Token',['type','value'])
	#
	scanner = pat.scanner(text)
	for m in iter(scanner.match,None):
		yield Token(m.lastgroup,m.group())


def parse_token():
	text = 'foo = 23 + 42 * 10'
	tokens = [('NAME', 'foo'), ('EQ','='), ('NUM', '23'), ('PLUS','+'),('NUM', '42'), ('TIMES', '*'), ('NUM', '10')]
	
	NAME = r'(?P<NAME>[a-zA-Z][a-zA-Z_0-9]*)'
	NUM = r'(?P<NUM>\d+)'
	PLUS = r'(?P<PLUS>\+)'
	TIMES = r'(?P<TIMES>\*)'
	EQ = r'(?P<EQ>=)'
	WS = r'(?P<WS>\s+)'
	
	master_pat = re.compile('|'.join([NAME,NUM,PLUS,TIMES,EQ,WS]))
	scanner = master_pat.scanner(text)
	
	while True:
		try:
			mt = scanner.match()
			print(mt.lastgroup,mt.group())
		except:
			break
			
	'''
	NAME foo
	WS
	EQ =
	WS
	NUM 23
	WS
	PLUS +
	WS
	NUM 42
	WS
	TIMES *
	WS
	NUM 10
	'''
	
	for tok in generate_token(master_pat,text):
		print(tok)
	'''
	Token(type='NAME', value='foo')
	Token(type='WS', value=' ')
	Token(type='EQ', value='=')
	Token(type='WS', value=' ')
	Token(type='NUM', value='23')
	Token(type='WS', value=' ')
	Token(type='PLUS', value='+')
	Token(type='WS', value=' ')
	Token(type='NUM', value='42')
	Token(type='WS', value=' ')
	Token(type='TIMES', value='*')
	Token(type='WS', value=' ')
	Token(type='NUM', value='10')
	'''

	LT = r'(?P<LT><)'
	LE = r'(?P<LE><=)'
	EQ = r'(?P<EQ>=)'
	NUM = r'(?P<NUM>\d+)'
	
	# 注意解析顺序：<= < = num
	master_pat = re.compile('|'.join([LE,LT,EQ,NUM]))
	
	for tok in generate_token(master_pat,'<=1'):
		print(tok)
	'''
	Token(type='LE', value='<=')
	Token(type='NUM', value='1')
	
	'''
	
	PRINT = r'(?P<PRINT>print)'
	NAME = r'(?P<NAME>[a-zA-Z_0-9]*)'

	master_pat = re.compile('|'.join([PRINT,NAME]))
	
	for tok in generate_token(master_pat,'printer'):
		print(tok)

	'''
	Token(type='PRINT', value='print')
	Token(type='NAME', value='er')
	Token(type='NAME', value='')
	'''

if __name__=="__main__":
	try:
		# test_html()
		parse_token()
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)



