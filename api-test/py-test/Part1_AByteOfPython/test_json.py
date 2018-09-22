#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/14'
Info:
        
"""

import os,json

if __name__=="__main__":
	try:
		localfile='/Users/huhao/software/idea_proj/data-base/api-test/python-test/Part1_AByteOfPython/stu.data'
		json_data = {'name':'Tom','age':12,'info':{'address':'beijing'}}
		
		cmd = "rm -rf {localfile}".format(localfile=localfile)
		os.system(cmd)
		
		# python 对象与文件间的转换
		with open(localfile,'wb') as f:
			json.dump(json_data,f) # dict => file 对象序列化到文件
			f.close()
		
		with open(localfile,'rb') as f:
			json_data2 = json.load(f) # file => dict 文件反序列化成对象
			print(json_data2)
			f.close()

		# python对象与字符串间的转换
		'''
		def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
            allow_nan=True, cls=None, indent=None, separators=None,
            encoding='utf-8', default=None, sort_keys=False, **kw):
		'''
		j2 = json.dumps(json_data,skipkeys=['name','age']) # dict => str python对象序列化成字符串
		print(j2)
		
		'''
		def loads(s, encoding=None, cls=None, object_hook=None, parse_float=None,
            parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
		'''
		j22 = json.loads(j2) # str => dict 字符串回复称python对象
		print(j22['name'])
		
	finally:
		os._exit(0)















