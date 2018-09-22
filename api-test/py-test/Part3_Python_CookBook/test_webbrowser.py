#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,webbrowser

def test_open():
	success = webbrowser.open('http://www.python.org')
	print(success) # True
	
	webbrowser.open_new('http://www.python.org') # 继承旧session,并刷新
	
	webbrowser.open_new_tab('http://www.python.org') # 标签页打开

def special_browser():
	c = webbrowser.get('chrome') # 选择在 指定浏览器打开
	c.open('http://www.python.org')


if __name__=="__main__":
	try:
		# test_open()
		special_browser()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




