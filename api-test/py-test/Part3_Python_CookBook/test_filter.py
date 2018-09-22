#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback,math
from operator import itemgetter
from itertools import compress



'''
itemgetter从dict 取出指定 key 进行排序

'''

def do_filter():
	values = ['1', '2', '-3', '-', '4', 'N/A', '5']
	res = list()
	# 基于try-catch 机制过滤异常
	for i in values:
		try:
			res.append(int(i))
		except:
			print('{i} is not an integer!'.format(i = i))
	print(res)
	
	pass

def get_sqrt():
	'''
	取数据同时，执行业务
	:return:
	'''
	mylist = [1, 4, -5, 10, -7, 2, 3, -1]
	print([math.sqrt(math.fabs(x)) for x in mylist])
	
def set_default():
	# 指定替换
	mylist = [1, 4, -5, 10, -7, 2, 3, -1]
	clip_neg = [n if n > 0 else 0 for n in mylist]
	print(clip_neg)
	# [1, 4, 0, 10, 0, 2, 3, 0]
	
def do_filter2():
	mylist = [1, 4, -5, 10, -7, 2, 3, -1]
	gt5 = [n>1 for n in mylist]
	print(gt5) # [False, True, False, True, False, True, True, False]
	print(list(compress(mylist,gt5))) # [4, 10, 2, 3], 过滤复合


if __name__=="__main__":
	try:
		mylist = [1, 4, -5, 10, -7, 2, 3, -1]
		sub_list = [n for n in mylist if n>0]
		print(type(sub_list)) # <class 'list'>
		print(sub_list) # [1, 4, 10, 2, 3]
		
		pos = (n for n in mylist if n>0) # 生成器策略可以节省内存
		print(type(pos)) # <class 'generator'>
		print(list(pos)) # 通过list 包裹生成器 取出数据
		
		do_filter()
		get_sqrt()
		
		set_default()
		
		do_filter2()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


