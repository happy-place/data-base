#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback
from operator import itemgetter
from itertools import groupby,chain
from collections import defaultdict


'''
itemgetter从dict 取出指定 key 进行排序

'''


def do_groupby():
	rows = [
		{'address': '5412 N CLARK', 'date': '07/01/2012'},
		{'address': '5148 N CLARK', 'date': '07/04/2012'},
		{'address': '5800 E 58TH', 'date': '07/02/2012'},
		{'address': '2122 N CLARK', 'date': '07/03/2012'},
		{'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
		{'address': '1060 W ADDISON', 'date': '07/02/2012'},
		{'address': '4801 N BROADWAY', 'date': '07/01/2012'},
		{'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
		]
	
	# 必须先执行排序，然后才能执行分组
	rows.sort(key=itemgetter('date'))
	for date,items in groupby(rows,key=itemgetter('date')):
		print(date)
		for i in items:
			print('\t',i)
	'''
	07/01/2012
	     {'address': '5412 N CLARK', 'date': '07/01/2012'}
	     {'address': '4801 N BROADWAY', 'date': '07/01/2012'}
	07/02/2012
		 {'address': '5800 E 58TH', 'date': '07/02/2012'}
		 {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}
		 {'address': '1060 W ADDISON', 'date': '07/02/2012'}
	07/03/2012
		 {'address': '2122 N CLARK', 'date': '07/03/2012'}
	07/04/2012
		 {'address': '5148 N CLARK', 'date': '07/04/2012'}
		 {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}
	'''
	
def get_partition():
	rows = [
		{'address': '5412 N CLARK', 'date': '07/01/2012'},
		{'address': '5148 N CLARK', 'date': '07/04/2012'},
		{'address': '5800 E 58TH', 'date': '07/02/2012'},
		{'address': '2122 N CLARK', 'date': '07/03/2012'},
		{'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
		{'address': '1060 W ADDISON', 'date': '07/02/2012'},
		{'address': '4801 N BROADWAY', 'date': '07/01/2012'},
		{'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
		]
	
	rows_by_date = defaultdict(list) # 先按date创建分区，然后到指定分区取数据即可
	for row in rows:
		rows_by_date[row['date']].append(row)
		
	print(rows_by_date['07/02/2012'])
		
	
def multi_loop():
	l1 = [1,2,3,4]
	s2 = {'a','b','c'}
	d3 = {'name':'tom','age':10}
	
	# 在不合并集合情况写，使用一次循环对多个集合进行遍历操作，如果是 dict 类型的集合，遍历的是keys()
	for x in chain(l1,s2,d3):
		print(x)
		'''
		1
		2
		3
		4
		b
		c
		a
		name
		age
		'''
	
	
	
if __name__=="__main__":
	try:
		
		# do_groupby()
		# get_partition()
		multi_loop()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
