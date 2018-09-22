#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,logging
from functools import wraps

def logged(level,name=None,message=None):
	def decorate(func):
		logname = name if name else func.__module__
		log = logging.getLogger(logname)
		logmsg = message if message else func.__name__
	
		@wraps(func)
		def wrapper(*args,**kwargs):
			log.log(level,logmsg)
			return func(*args,**kwargs)
		return wrapper
	return decorate


@logged(logging.DEBUG) # 对 logged 进行入参，并将 add 赋值给 func，对 wrapper 传入 x,y
def add(x,y):
	return x + y

@logged(logging.CRITICAL,'example')
def spam():
	print('Spam')



@logged(logging.DEBUG)
def func(x,y,z): # 等效于 logged(logging.DEBUG)(func)
	pass

if __name__=="__main__":
	try:
		print(add(1,2))
		spam()
		
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




