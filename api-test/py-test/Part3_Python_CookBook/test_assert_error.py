#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,unittest,errno


def parse_int(s):
	return int(s)

class TestConversion(unittest.TestCase):
	def test_bad_int(self):
		# 当入参为 'N/A' 时 parse_int 会报ValueError 异常
		self.assertRaises(ValueError,parse_int,'N/A')


class TestConversion2(unittest.TestCase):
	def test_bad_int(self):
		# 通过手动捕捉异常进行进行单元测试，需要注意，为防止遗漏其他异常，要设置 else: self.fail()
		try:
			parse_int('N/A')
		except ValueError as e:
			self.assertEqual(type(e),ValueError)
		else:
			self.fail('ValueError not raised')


class TestConversion3(unittest.TestCase):
	def test_bad_int(self):
		# parse_int('N/A') 调用时会触发ValueError 异常，异常信息为invalid literal .* 正则通配
		# self.assertRaisesRegex(ValueError, 'invalid literal .*',parse_int, 'N/A')
		
		# 当做上下文管理器使用，等同于上面代码
		with self.assertRaisesRegex(ValueError,'invalid literal .*'): # 无效字面量
			r = parse_int('N/A')


class TestIO(unittest.TestCase):
	def test_file_not_found(self):
		try:
			# f = open('test_args_in_metacls.py','r') # 正常打开
			f = open('/aa/bb/cc') # 激活异常
		except IOError as e:
			self.assertEqual(e.errno,errno.ENOENT) # 判断具体异常是否是预期的
			print(e.errno,errno.ENOENT) # ENOENT = Error NOt ENTry. 就是路径不存在的意思
		else:
			self.fail('IOError not raised') # AssertionError: IOError not raised
		
		

if __name__=="__main__":
	try:
		unittest.main()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




