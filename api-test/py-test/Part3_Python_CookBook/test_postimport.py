#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from functools import wraps

from postimport import when_imported

# 执行 import threading 操作时触发 报警


def test_thread():
	# import threading
	pass


def logged(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		print('Calling', func.__name__,args,kwargs)
		return func(*args,**kwargs)
	return wrapper

@when_imported('math')
def add_logging(mod):
	mod.cos  = logged(mod.cos)
	mod.sin = logged(mod.sin)


def test_import_math():
	import math
	# add_logging(math)
	math.cos(math.pi/2) # Calling cos (1.5707963267948966,) {}



if __name__=="__main__":
	try:
		# test_thread()
		
		# test_import_math()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




