#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/14'
Info:
        
"""

import pickle,os,sys

if __name__=="__main__":
	try:
		localfile='/Users/huhao/software/idea_proj/data-base/api-test/python-test/Part1_AByteOfPython/stu.data'
		data = ["apple",'orange','banana']
		
		cmd = "rm -rf {localfile}".format(localfile=localfile)
		os.system(cmd)
		
		# python 对象与文件间的转换
		with open(localfile,'wb') as f:
			sp = pickle.dump(data,f) # dict => file 对象序列化到文件
			print('sp',sp)
			f.close()
		
		with open(localfile,'rb') as f:
			data1 = pickle.load(f) # file => dict 文件反序列化成对象
			print(data1)
			f.close()

		# python对象与字符串间的转换
		j1 = {"a":1,"b":2}
		j2 = pickle.dumps(j1) # dict => str python对象序列化成字符串
		print(j2)
		
		j22 = pickle.loads(j2) # str => dict 字符串回复称python对象
		print(j22['a'])
		
	finally:
		os._exit(0)















