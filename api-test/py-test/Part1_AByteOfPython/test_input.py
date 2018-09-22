#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/16'
Info:
        
"""

import os,traceback

# 逆转
def reverse(text):
	return text[::-1]

# 检测是否是回文
def is_palindrome(text):
	return text == reverse(text)


if __name__=="__main__":
	
	try:
		text = input("Please Enter a text: ")
		print(is_palindrome(text))
		
	
	
	except:
		traceback.print_exc()
	finally:
		os._exit(0)

	


