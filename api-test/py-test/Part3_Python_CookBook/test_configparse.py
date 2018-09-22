#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,sys
from configparser import ConfigParser

def do_parse():
	cfg = ConfigParser()
	cfg.read('config1.ini')
	sections = cfg.sections()
	print(sections)
	
	library = cfg.get('installation','library')
	print(library)
	
	log_errors = cfg.getboolean('debug','log_errors')
	print(log_errors)
	
	port = cfg.getint('server','port')
	print(port)
	
	nworkers = cfg.getint('server','nworkers')
	print(nworkers)
	
	signature = cfg.get('server','signature')
	print(signature)

	'''
	['installation', 'debug', 'server']
	/usr/local/lib
	True
	8080
	32
	=================================
	Brought to you by the Python Cookbook
	=================================
	
	'''

	cfg.set('server','port','9000')
	cfg.set('debug','log_errors','False')
	cfg.write(sys.stdout) # 写出到控制台
	
	# with open('config.ini','w') as f: # 写出到文件
	# 	cfg.write(f)
	
	
	# config.ini 源文件中 prefix = /usr/local 与 prefix: /usr/local 是等价的 赋值语句，放在最前和最后都行
	
	# config.ini 中 boolean 类型 true True Yes 1 是等价的
	
def test_layer():
	cfg = ConfigParser()
	cfg.read(['config1.ini','config2.ini']) # 物理存储上属于连个，但逻辑上属于一个
	sections = cfg.sections()
	print(sections) # ['installation', 'debug', 'server']
	
	prefix = cfg.get('installation','prefix')
	print(prefix) # /Users/beazley/test 以最后的为准
	
	signature = cfg.get('server','signature')
	print(signature)



if __name__=="__main__":
	try:
		# do_parse()
		test_layer()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




