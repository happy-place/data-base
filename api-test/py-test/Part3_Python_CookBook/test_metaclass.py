#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/4'
Info:
    通过元类控制实例的创建
"""
import os,traceback,weakref

# 类实例创建 方案1： 直接基于初始化方法 __init__ 创建
class Spam:
	def __init__(self,name):
		self.name = name

# 基于元类 __call__ 方法创建，此处屏蔽了创建对象唯一通道 __call__ ，因此 Factory 不能创建任何实例，只能以工程类形式存在
class NoInstances(type):
	def __call__(self, *args, **kwargs):
		raise TypeError("Can't instantiate directly")

class Factory(metaclass=NoInstances):
	@staticmethod
	def grok(x):
		print('Spam grok')


def test_instance():
	a = Spam('aa')
	Factory.grok(42)
	# b = Factory() # 触发__call__ TypeError: Can't instantiate directly

class Singleton(type):
	def __init__(self,*args,**kwargs):
		self.__instance = None
		super().__init__(*args,**kwargs)
	
	def __call__(self, *args, **kwargs):
		if self.__instance is None:
			self.__instance = super().__call__(*args, **kwargs)
		return self.__instance

class Spam3(metaclass=Singleton):
	def __init__(self):# 创建对象时，先进入 元类的 __call__，然后通过 super().__call__ 回调到此，最后返回
		print('Creating Spam')

def test_singleton():
	a = Spam3() # Singleton.__call__ 》 Spam3.__init__ 》Singleton.__call__ 》 。
	b = Spam3()
	print(a)
	print(a is b)


#  缓存 + 元类 创建单例
class Cached(type):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.__cache = weakref.WeakValueDictionary()

	def __call__(self,*args):
		if args in self.__cache:
			print('fetch from cache')
			return self.__cache[args]
		else:
			obj = super().__call__(*args)
			self.__cache[args] = obj
			return obj

class Spam4(metaclass=Cached):
	def __init__(self,name):
		print('Creating Spam({!r})'.format(name))
		self.name = name

def test_cache():
	a = Spam4('aa') # Creating Spam('aa')
	b = Spam4('aa') # fetch from cache
	c = Spam4('aa') # fetch from cache
	print(a is b) # True
	print(a is c) # True
	

# 不使用元类情况下创建单例
class _Spam:
	def __init__(self):
		print('Creating Spam')

_spam_instance = None

def Spam():
	global _spam_instance
	if _spam_instance is not None:
		return _spam_instance
	else:
		_spam_instance = _Spam()
		return _spam_instance






if __name__=="__main__":
	try:
		# test_instance()
		# test_singleton()
		test_cache()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
