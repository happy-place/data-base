#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,logging
from functools import wraps,partial


logging.basicConfig(level=logging.DEBUG)

'''
为了这样做，我们使用了一个技巧，就是利用 functools.partial 。 它会返回一个未完全初始化的自身，除了被包装函数外其他参数都已经确定下来了
适应 @logged 无参注解 和 @logged(level=logging.CRITICAL,name='example') 带参注解
'''

def logged(func=None,*,level=logging.DEBUG,name=None,message=None):
	'''
	以下注解模式中 logged 没带(), 返回  partial(logged,level=level,name=name,message=message) 偏函数替代
	@logged
	def add(x,y):
	
	以下注解模式中 logged 带有(), 返回 wrapper
	@logged(level=logging.CRITICAL,name='example')
	def spam():
	
	:param func:
	:param level:
	:param name:
	:param message:
	:return:
	'''
	if func is None:
		return partial(logged,level=level,name=name,message=message)
	
	logname= name if name else func.__module__
	log = logging.getLogger(logname)
	logmsg = message if message else func.__name__
	
	@wraps(func)
	def wrapper(*args,**kwargs):
		log.log(level,logmsg)
		return func(*args,**kwargs)
	
	return wrapper

@logged
def add(x,y):
	return x + y # DEBUG:__main__:add

@logged(level=logging.CRITICAL,name='example')
def spam():
	print('Spam!')


if __name__=="__main__":
	try:
		add(1,3)
		spam()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




