#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/19'
Info:
        
"""

import os,traceback
from operator import itemgetter

def test_express():
	nums = [1,2,3,4,5]
	s = sum(x*x for x in nums)
	print(s) # 55


def chk_python():
	dir = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook'
	files = os.listdir()
	
	if any(name.endswith('.py') for name in files): # 只要一个元素满足条件，就都满足
		print("There be python.")
	else:
		print('Sorry, no python.')
	

def list_join():
	a = ['AA',12,34.5,True]
	print(','.join((str(x) for x in a))) # join 只能操作list(str)

def sum_from_list_dict():
	portfolio = [
		{'name':'GOOG', 'shares': 50},
		{'name':'YHOO', 'shares': 75},
		{'name':'AOL', 'shares': 20},
		{'name':'SCOX', 'shares': 65}
		]
	min_shares = min(s['shares'] for s in portfolio) # # 20
	min_shares = min(portfolio,key=lambda s:s['shares']) # {'name': 'AOL', 'shares': 20}
	min_shares = min(portfolio,key=itemgetter('shares')) # {'name': 'AOL', 'shares': 20}
	print(min_shares)


if __name__=="__main__":
	try:
		# test_express()
		# chk_python()
		# list_join()
		sum_from_list_dict()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)



