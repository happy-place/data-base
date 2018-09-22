#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/20'
Info:
        
"""
import os,traceback,re

def test_char():
	a = 'Hello World'
	print(a[0],a[1]) # H e
	b = b'Hello World'
	print(b[0],b[1]) # # 72 101
	print(b) # b'Hello World'
	print(b.decode('ascii')) # Hello World

def test_decode():
	b = b'Hello World'
	print(b) # b'Hello World'
	print(b.decode('ascii')) # Hello World
	# b'AAA               100     490.10'
	print('{:10s} {:10d} {:10.2f}'.format('AAA',100,490.1).encode('ascii'))


def test_re():
	'''
	使用正则对字节型字符串进行切分，正则表达式也必须使用 b''
	:return:
	'''
	data = b'FOO:BAR,SPAM'
	try:
		print(re.split('[:,]',data))
	except:
		print("print(re.split('[:,]',data)) <<<< split error!")
		print(re.split(b'[:,]',data)) # [b'FOO', b'BAR', b'SPAM']
	

def bytearray_opt():
	data = bytearray(b'Hello World')
	print(data[0:5]) # bytearray(b'Hello')
	print(data.startswith(b'Hello')) # True
	print(data.split(b" ")) # [bytearray(b'Hello'), bytearray(b'World')]
	print(data.replace(b'Hello',b'Hello Cruel')) # bytearray(b'Hello Cruel World')
	
	pass


def bytestr_opt():
	'''
	字符串上的绝大部分操作也适用于字节型字符串
	:return:
	'''
	data = b'Hello world'
	print(data[0:5]) # b'Hello'
	print(data.startswith(b'Hello')) #True
	print(data.split(b' ')) # [b'Hello', b'world']
	print(data.replace(b'Hello',b'Hello Cruel')) # b'Hello Cruel world'
	
	pass


if __name__=="__main__":
	try:
		
		# bytearray_opt()
		# bytearray_opt()
		# test_re()
		# test_char()
		test_decode()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


