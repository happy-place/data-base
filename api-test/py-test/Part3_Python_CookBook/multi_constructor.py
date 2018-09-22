#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,time

class Date:
	def __init__(self,year,month,day):
		self.year = year
		self.month = month
		self.day = day
	
	@classmethod  # 静态方法 和 类方法都可被继承
	def today(cls):
		'''
		本质是上还是通过cls() 调用到主构造器
		:return:
		'''
		t = time.localtime()
		return cls(t.tm_year,t.tm_mon,t.tm_mday)
	
	@classmethod
	def today2(cls):
		d = cls.__new__(cls) # 通过反射先床架实例，然后注入属性
		t = time.localtime()
		d.year = t.tm_year
		d.month = t.tm_mon
		d.day = t.tm_mday
		return d
	
	
	
	def __str__(self):
		return '{}({})'.format(self.__class__.__name__,'-'.join([str(self.year),str(self.month),str(self.day)]))
		
		
	@staticmethod
	def say_hello():
		print('hello')
	
def test_init():
	a = Date(2018,8,1) # 通过主构造器创建实例
	b = Date.today() # 通过类方法构造实例
	print(a,b) # Date(2018-8-1) Date(2018-8-1)
	
	c  = Date.today2()
	print(c)

# 通过继承获取父类 多个构造器
class NewDate(Date):
	pass

def test_new():
	c = Date.today()
	d = NewDate.today()
	print(c,d)
	d.say_hello()







if __name__=="__main__":
	try:
		test_init()
		# test_new()
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




