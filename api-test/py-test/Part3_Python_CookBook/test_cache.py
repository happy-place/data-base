#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,logging,weakref


def test_logging():
	'''
	getLogger 如果已经存在就直接获取，否则就创建新的
	:return:
	'''
	a = logging.getLogger('foo')
	b = logging.getLogger('bar')
	c = logging.getLogger('foo')
	print(a is b) # False
	print(a is c) # True
	
	

class Spam:
	def __init__(self,name):
		self.name = name

_spam_cache = weakref.WeakValueDictionary()

def get_spam(name):
	if name not in _spam_cache:
		print('do caching ... ')
		s = Spam(name)
		_spam_cache[name] = s
	else:
		s = _spam_cache[name]
	return s

def test_cache():
	# 首次请求，会创建缓存
	sa = get_spam('foo')
	sb = get_spam('bar')
	
	# 再次请求，直接从缓存提取
	sc = get_spam('foo')
	
	print(sa is sb)
	print(sa is sc)
	
	del sb # 删除唯一引用，会从缓存中被剔除
	print(list(_spam_cache)) # ['foo']
	
	del sa # 减少一个引用，会继续保存在缓存中
	print(list(_spam_cache)) # ['foo']
	
	del sc # 删除最后一个引用，缓存消失
	print(list(_spam_cache)) # ['foo']
	
	
'''
缓存代码与类耦合
'''
class Spam2:
	# 类属性定义在方法之外，通过 cls.field 调用
	_spam_cache = weakref.WeakValueDictionary()
	
	# 负责创建对象，必须有返会值
	def __new__(cls, name):
		if name in cls._spam_cache:
			return cls._spam_cache[name] # 通过 cls.classfield 方法调用类属性
		else:
			self = super().__new__(cls) # 创建对象
			cls._spam_cache[name] = self
			return self
	
	# 负责初始化 __new__创建的对象，无返回值，相当于 setter
	def __init__(self,name):
		print('Initializing Spam')
		self.name = name
	

def test_new():
	sa = Spam2('foo') # Initializing Spam
	sb = Spam2('bar') # Initializing Spam
	sc = Spam2('foo') # Initializing Spam # 即便从缓存中提取，也会被初始化

	print(sa is sb) # False
	print(sa is sc) # True
	

class CacheManager:
	def __init__(self):
		self._cache = weakref.WeakValueDictionary()
	
	def get_spam(self,name):
		if name not in self._cache:
			s = Spam3(name)
			self._cache[name] = s
		else:
			s = self._cache[name]
		return s
	
	def clear(self):
		self._cache.clear()
	
class Spam3:
	'''
	通过缓存管理器维护缓存对象，如果已经缓存，则不会再被初始化，存在的问题是，直接将 __init__ 实例化器暴露给用户，用户很可能不走缓存方法 get_spam
	而直接通过 __init__ 实例化器创建对象
	回避策略：
		1. 类名首字母下划线开头 _Spam3 显式提现用户无需手动实例化，而是可以通过缓存策略获取
		2. 实现 __init__ 时直接 抛出异常，让其不能直接被实例化，而是必须通过缓存工厂函数获取
	'''
	manager = CacheManager()
	def __init__(self,name):
		print('do Init ...')
		self.name = name
	def get_spam(name):
		return Spam3.manager.get_spam(name)

def test_manager():
	a  =Spam3.get_spam('foo') # do Init ...
	b  =Spam3.get_spam('bar') # do Init ...
	c  =Spam3.get_spam('foo')
	
	print(a is b) # False
	print(a is c) # True


class Spam4:
	'''
	通过工厂函数 _new 而非 初始化函数__init__ 创建实例对象
	'''
	def __init__(self,name):
		raise RuntimeError("Can't instantiate directly ,please use get_spam(name) which can use cache strategy.")
	
	@classmethod
	def _new(cls,name):
		self = cls.__new__(cls)
		self.name = name
		return self

def test_init():
	a  =Spam4._new('foo')
	b  =Spam4._new('bar') # do Init ...
	c  =Spam4._new('foo')
	
	# a = Spam4('neer') # RuntimeError: Can't instantiate directly ,please use get_spam(name) which can use cache strategy.
	
	print(a is b) # False
	print(a is c) # False # 为启用缓存，实质是不同的对象


class CachedSpamManager2:
	def __init__(self):
		self._cache = weakref.WeakValueDictionary()
	
	def get_spam(self,name):
		if name not in self._cache:
			temp = Spam4._new(name)
			self._cache[name] = temp
		else:
			temp = self._cache[name]
		return temp
	
	def clear(self):
		self._cache.clear()

def test_CachedSpamManager2():
	'''
	缓存管理器通过访问工厂函数，创建对象
	:return:
	'''
	m = CachedSpamManager2()
	a = m.get_spam('foo')
	b = m.get_spam('bar')
	c = m.get_spam('foo')
	
	print(a is b) # False
	print(a is c) # True


if __name__=="__main__":
	try:
		# test_cache()
		# test_new()
		# test_manager()
		# test_init()
		test_CachedSpamManager2()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




