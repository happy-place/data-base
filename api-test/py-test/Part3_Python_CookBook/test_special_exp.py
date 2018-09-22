#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
skip() 装饰器能被用来忽略某个你不想运行的测试。 skipIf() 和 skipUnless()
对于你只想在某个特定平台或Python版本或其他依赖成立时才运行测试的时候非常有用。
 使用 @expected 的失败装饰器来标记那些确定会失败的测试，并且对这些测试你不想让测试框架打印更多信息
        
"""
import os,traceback,unittest,platform

class Tests(unittest.TestCase):
	def test_0(self):
		self.assertTrue(True) # 自动跳过
	
	@unittest.skip('skipped test')
	def test_1(self):
		self.fail('should have failed!') # 原本会抛异常，但通过skip 跳过异常
	
	@unittest.skipIf(os.name=='posix','Not supported on Unix') # 系统为 Unix 时，跳过异常检测，因为只能在win环境执行导入
	def test_2(self):
		import cygwinreg
	
	@unittest.skipUnless(platform.system() =='Darwin','Mac specific test') # 除非在Mac 环境才执行异常检验
	def test_3(self):
		self.assertTrue(True)
	
	@unittest.expectedFailure # 预期会跑一次，如果政策执行则报错
	def test_4(self):
		self.assertEqual(2+2,5)



if __name__=="__main__":
	try:
		unittest.main()
		'''
		python3 test_special_exp.py -v
		test_0 (__main__.Tests) ... ok
		test_1 (__main__.Tests) ... skipped 'skipped test'
		test_2 (__main__.Tests) ... skipped 'Not supported on Unix'
		test_3 (__main__.Tests) ... ok
		test_4 (__main__.Tests) ... expected failure

		'''
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




