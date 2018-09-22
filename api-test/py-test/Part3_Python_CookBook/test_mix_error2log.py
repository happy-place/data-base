#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,unittest,sys,errno

class MyTest(unittest.TestCase):
	def test_file_not_found(self):
		try:
			# f = open('test_args_in_metacls.py','r') # 正常打开
			f = open('/aa/bb/cc') # 激活异常
		except IOError as e:
			self.assertEqual(e.errno,errno.ENOENT) # 判断具体异常是否是预期的
			print(e.errno,errno.ENOENT) # ENOENT = Error NOt ENTry. 就是路径不存在的意思
		else:
			self.fail('IOError not raised') # AssertionError: IOError not raised
	pass

def main(out=sys.stderr,verbosity=2):
	loader = unittest.TestLoader()
	suite = loader.loadTestsFromTestCase(sys.modules[__name__])
	unittest.TextTestRunner(out,verbosity=verbosity).run(suite)



if __name__=="__main__":
	try:
		with open('testing.out','w') as f:
			main(f)
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




