#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:




"""
import os,traceback,importlib

def test_importlib():
	'''
	使用importlib.import_module()函数来手动导入名字为字符串给出的一个模块或者包的一部分
	
	:return:
	'''
	
	
	math = importlib.import_module('math')
	print(math.sin(2)) # 0.9092974268256817
	
	url = importlib.import_module('urllib.request')
	data = url.urlopen('http://www.baidu.com')
	print(data.read())
	data.close()



if __name__=="__main__":
	try:
		test_importlib()
	
	
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




