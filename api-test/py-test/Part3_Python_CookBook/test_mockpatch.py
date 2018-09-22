#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,io,unittest

from unittest.mock import MagicMock
from unittest.mock import patch
import example


# 基于注解调试
# @patch 注解，注释的函数，自动赋值给 mock_func
@patch('example.func')
def test1(x,y, mock_func):
	example.func(x,y)       # Uses patched example.func
	mock_func.assert_called_with(x,3)

# 基于上下文管理器调试
def test2(x,y):
	with patch('example.func') as mock_func:
		example.func(x,y)
		# 断言前面函数调用的入参是 x,y
		mock_func.assert_called_with(x,y)

# 手动调试
def test3(x,y):
	p = patch('example.func')
	mock_func = p.start()
	example.func(x,y)
	mock_func.assert_called_with(x,3)
	p.stop()


# 多上下文补丁
@patch('example.func1')
@patch('example.func2')
@patch('example.func3')
def multi_patch(x,y,mock_func1,mock_func2,mock_func3):
	example.func1(x,y)
	mock_func1.assert_called_with(x,y)
	example.func2(x,y)
	mock_func2.assert_called_with(x,y)
	example.func3(x,y)
	mock_func3.assert_called_with(x,3)


def multi_patch2(x,y):
	with patch('example.func1') as mock_func1, patch('example.func2') as mock_func2, \
			patch('example.func3') as mock_func3:
		
		example.func1(x,y)
		mock_func1.assert_called_with(x,y)
		example.func2(x,y)
		mock_func2.assert_called_with(x,y)
		example.func3(x,y)
		mock_func3.assert_called_with(x,3)

def test_magic_mock():
	print(x) # 42
	with patch('__main__.x'):
		print(x) # <MagicMock name='x' id='4447470144'>
	print(x) # 42

def do_replace():
	print(x) # 42
	with patch('__main__.x','hello world'):
		print(x) # hello world 被替换成为 'hello world'
	print(x) # 42

'''
被用来作为替换值的 MagicMock 实例能够模拟可调用对象和实例。 他们记录对象的使用信息并允许你执行断言检查
'''
def test_magic_mock():
	m = MagicMock(return_value = 10) # 模拟函数调用怎么都返回 10
	val = m(1,2,debug=True)
	print(val) # 10
	m.assert_called_with(1,2,debug=True)  # 断言m 被调用的入参，缺少debug=True 时会报错
	
	m.upper.return_value = 'HELLO' # 当调用m 实例的upper 函数时，返回值为 'HELLO'
	print(m.upper('hello'))
	assert m.upper.called # 断言 m 的 upper 函数被调用了
	
	m.split.return_value = ['hello','world']
	print(m.split('hello world')) # ['hello', 'world']
	m.split.assert_called_with('hello world')
	
	print(m['blah']) # <MagicMock name='mock.__getitem__()' id='4420051856'> 字段创建了模拟对象
	print(m.__getitem__.called) # True 测试基于key 取值是否被调用了
	m.__getitem__.assert_called_with('blah') # 测试入参是否一致
	

def dowprices():
	data = example.get_json()
	
	return data

sample_data = {'IBM':91.1,'AA': 13.25,'MSFT':27.72}

class Tests(unittest.TestCase):
	@patch('example.get_json',return_value=sample_data)
	def test_dow(self,mock_urlopen): # mock_urlopen 被赋值为 example.get_json，且在被注解的函数中，被设置强制返回sample_data
		p = dowprices() # 此处被强制返回了sample_data
		self.assertTrue(mock_urlopen.called) # 断言  example.get_json 被调用了
		self.assertEqual(p,{'IBM':91.1,'AA': 13.25,'MSFT':27.72}) # 断言返回值与 给的值一致
		
if __name__=="__main__":
	try:
		# test1(1,2)
		# test2(1,2)
		# test3(1,2)
		
		# multi_patch(1,2)
		# multi_patch2(1,2)
		
		x= 42
		# test_magic_mock()
		# do_replace()
		# test_magic_mock()
		
		unittest.main() # 凡是 unittest.TestCase 相关子类都将被调用
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




