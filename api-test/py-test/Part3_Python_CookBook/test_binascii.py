#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/25'
Info:
        
"""

import os,traceback,binascii,base64

def test_encode_decode():
	'''
	注：base64.b16decode/b16encode() 只能操作大写形式十六进制字母，而 binascii 大小写都能处理
	:return:
	'''
	
	s = b'hello'
	
	# binascii
	hex_str = binascii.b2a_hex(s)
	print(hex_str) # b'68656c6c6f'  字节字符串 -> 十六进制 编码
	print(hex_str.decode('ascii')) # 68656c6c6f 使用 unicode编码,强制输出十六进制字符串
	
	real_str = binascii.a2b_hex(hex_str)
	print(real_str) # b'hello' 十六进制 -> 字节字符串 解码
	
	base_str = base64.b16encode(s)
	print(base_str) # b'68656C6C6F'
	
	real_str = base64.b16decode(base_str)
	print(real_str) # b'hello'
	
	# Base64格式编解码二进制数据
	b64_str = base64.b64encode(s)
	print(b64_str) # b'aGVsbG8='
	print(b64_str.decode('ascii'))
	
	
	real_str = base64.b64decode(b64_str)
	print(real_str) # b'hello'
	
	
	
	




if __name__=="__main__":
	try:
		test_encode_decode()
		
		
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)



