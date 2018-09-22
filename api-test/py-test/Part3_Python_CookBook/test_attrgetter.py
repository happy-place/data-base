#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""


import os,traceback
from operator import attrgetter
'''
依据指定类的属性，进行排序

'''

class User:
	def __init__(self,uid):
		self.uid = uid
	
	def __repr__(self):
		return 'User({!r})'.format(self.uid)




def do_sort():
	users = [User(23),User(3),User(99)]
	print(users)
	print(sorted(users,key=lambda u:u.uid))    # [User(3), User(23), User(99)]
	print(sorted(users,key=attrgetter('uid'))) # [User(3), User(23), User(99)]




if __name__=="__main__":
	try:
		
		do_sort()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


