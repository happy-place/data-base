#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
	通过钩子远程加载模块
	
1).server 端创建如下代码结构
	testcode/
	    spam.py
	    fib.py
	    grok/
	        __init__.py
	        blah.py

    -----------------------
	# spam.py
	print("I'm spam")
	
	def hello(name):
	    print('Hello %s' % name)
	
	# fib.py
	print("I'm fib")
	
	def fib(n):
	    if n < 2:
	        return 1
	    else:
	        return fib(n-1) + fib(n-2)
	
	# grok/__init__.py
	print("I'm grok.__init__")
	
	# grok/blah.py
	print("I'm grok.blah")
	-----------------------

2).server 端通过http协议发布代码
	cd /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/testcode
	python3 -m http.server 15000  (将当前目录下的内容发布到 localhost:15000 下)
	通过 http://localhost:15000 在浏览器可访问到如下代码结构
			fib.py
			grok/
			spam.py

3).client 端，通过 urllib.request 的 urlopen() 函数读取文件信息，完成远程模块加载基础工作

	
"""
import os,traceback,imp,sys,logging
import urlimport

logging.basicConfig(level=logging.DEBUG)

from urllib.request import urlopen

# 测试远程抓取模块文件信息
def fetch_data():
	u = urlopen('http://localhost:15000/fib.py')
	data = u.read().decode('utf-8')
	print(data)
	u.close()


def load_module(url):
	# http 远程抓取脚本
	u = urlopen(url)
	source = u.read().decode('utf-8')
	u.close()
	
	# 对脚本进行编译
	code = compile(source,url,'exec')
	
	# 将编译后的脚本信息与本地环境进行整合
	mod = sys.modules.setdefault(url,imp.new_module(url))
	mod.__file__ = url
	mod.__package__ = ''
	exec(code,mod.__dict__)
	
	# 返回远程加载脚本
	return mod
	

def test_remote_load():
	fib = load_module('http://localhost:15000/fib.py')
	res = fib.fib(12)
	print(res)
	'''
	I'm fib
	233
	'''
	
	blah = load_module('http://localhost:15000/grok/blah.py')
	blah.say_hi('hello world!')
	'''
	I'm grok.blah
	hello world!
	'''

def test_utlimport():
	urlimport.install_meta('http://localhost:15000')
	import fib
	
	res = fib.fib(12)
	print(res)
	
	import grok.blah as blah
	blah.say_hi('hello world')
	'''
	I'm grok.blah
	hello world
	'''

def test_syspath():
	urlimport.install_path_hook()
	sys.path.append('http://localhost:15000')
	import fib
	
	res = fib.fib(12)
	print(res)
	'''
	I'm fib
	233
	'''


if __name__=="__main__":
	try:
		# fetch_data()
		# test_remote_load()
		# test_utlimport()
		test_syspath()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




