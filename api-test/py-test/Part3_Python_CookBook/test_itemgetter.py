#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""

import os,traceback
from operator import itemgetter
'''
itemgetter从dict 取出指定 key 进行排序

'''

def do_sort():
	rows = [
		{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
		{'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
		{'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
		{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
		]

	rows_by_fname = sorted(rows,key=itemgetter('fname')) # 基于 fname 排序 等效于
	rows_by_fname1 = sorted(rows,key=lambda a:a['fname'])
	print(rows_by_fname1)
	'''
	[{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]
	'''
	
	rows_by_uid = sorted(rows,key=itemgetter('uid')) # 基于 uid 排序 等效于
	rows_by_uid1 = sorted(rows,key=lambda a:a['uid'])
	print(rows_by_uid1)
	'''
	[{'fname': 'John', 'lname': 'Cleese', 'uid': 1001}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}]
	'''
	
	rows = [
		{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
		{'fname': 'Brian', 'lname': 'Beazley', 'uid': 1002},
		{'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
		{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
		]
	
	rows_by_fname_uid = sorted(rows,key=itemgetter('fname','uid')) # 基于 fname，uid 排序 等效于
	rows_by_fname_uid1 = sorted(rows,key=lambda a:(a['fname'],a['uid']))
	print(rows_by_fname_uid1)
	'''
	[{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, {'fname': 'Brian', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]
	'''


if __name__=="__main__":
	try:
	
		do_sort()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


