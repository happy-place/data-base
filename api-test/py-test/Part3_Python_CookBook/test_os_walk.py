#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,sys,time

def findfile(start,name):
	# 给定顶级目录 start 和 待查找文件名name，通过 os.walk() 依次递归向下查找，每次都要返回 当前查找，相对于顶层目录的相对位置 relpath
	# 以及此相对位置位置下，存在的 全部文件files 和 文件目录dirs
	for relpath,dirs,files in os.walk(start):
		if name in files:
			full_path = os.path.join(start,relpath,name) # 凭借全路径返回
			print(os.path.normpath(os.path.abspath(full_path))) # os.path.normpath '/aa//vv/cc/../ss' -> /aa/vv/ss



def modfied_within(top, backseconds):
	now = time.time()
	
	for path,dirs,files in os.walk(top):
		for name in files:
			fullpath = os.path.join(path,name)
			if os.path.exists(fullpath):
				mtime = os.path.getmtime(fullpath)
				if mtime > (now - backseconds): # 最近5min修改过的 -300
					print(fullpath)
	




if __name__=="__main__":
	try:
		base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
		# findfile(base,'setup.py')
		
		
		modfied_within(base,300)
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




