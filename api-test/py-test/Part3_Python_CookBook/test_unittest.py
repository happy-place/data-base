#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

from io import StringIO
from unittest import TestCase



def urlprint(protocol,host,domain):
	url = '{}://{}.{}'.format(protocol,host,domain)
	print(url)

class TestURLPrint(TestCase):
	def test_url_gets_to_stdout(self):
		protocol = 'http'
		host='www'
		domain = 'python.org'
		expected_url = '{}://{}.{}\n'.format(protocol,host,domain)
		
		with patch('sys.stdout',new = StringIO()) as fake_out:
			urlprint(protocol,host,domain) # 通过sys.stdout -> fake_out
			self.assertEqual(fake_out.getvalue(),expected_url) # 将fake_out 与 expected_url 对比，一致返回Ok,否则返回差异点





if __name__=="__main__":
	try:
		# tp = TestURLPrint()
		# tp.test_url_gets_to_stdout()
		
		test1(1,2,example.func)
		
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




