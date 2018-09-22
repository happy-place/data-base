#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
	可自定义属性的装饰器
"""
import os,traceback,logging
from functools import wraps,partial

def attach_wrapper(obj,func=None):
	if func is None:
		return partial(attach_wrapper,obj)
	setattr(obj,func.__name__,func)
	return func


def logged(level,name=None,message=None):
	
	def decorate(func):
		logname = name if name else func.__module__
		log = logging.getLogger(logname)
		logmsg = message if message else func.__name__
		
		@wraps(func)
		def wrapper(*args,**kwargs):
			log.log(level,logmsg)
			return func(*args,**kwargs)
	
		'''
		在装饰器的基础上继续使用装饰器，用来动态修改装饰器的参数
		'''
		@attach_wrapper(wrapper)
		def set_level(newlevel):
			nonlocal level
			level = newlevel
		
		@attach_wrapper(wrapper)
		def set_message(newmsg):
			nonlocal logmsg
			logmsg = newmsg
		
		return wrapper
	return decorate
		

@logged(logging.DEBUG)
def add(x,y):
	return x + y

@logged(logging.CRITICAL,'example')
def spam():
	print('Spam')
		
	
def test_wrapper():
	
	logging.basicConfig(level=logging.DEBUG) # 设置基础日志级别
	
	add(2,3) # DEBUG:__main__:add
	
	add.set_message('Add called') # DEBUG:__main__:Add called
	add(2,3)
	
	add.set_level(logging.WARNING) # WARNING:__main__:Add called
	add(2,3)




if __name__=="__main__":
	try:
		test_wrapper()
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




