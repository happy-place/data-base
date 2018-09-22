#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/14'
Info:
        
"""
import os, sys

# from Part1_AByteOfPython import test_args
# from Part1_AByteOfPython import *


if __name__=="__main__":
	try:
		# a=1
		# os.dir(a)
		# del a
		# print(a)
		shoplist = ['apple','mango','carrot','banaa']
		print('I have ',len(shoplist),' items to purchase')
		print('These items are: ', ','.join(shoplist))
	
	finally:
		os._exit(0)