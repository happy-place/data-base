#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback
from collections import Counter


def get_times(items,key):
	'''
	取出指定key 出现的频次
	:param items:
	:param key:
	:return:
	'''
	wc = Counter(items)
	return wc[key]

def cal_wc(items,key):
	wc = dict()
	for it in items:
		if it in wc:
			wc[it] +=1
		else:
			wc[it] = 1
			
	if key in wc:
		return wc[key]
	else:
		return 0
	
def get_most(items,n=1):
	'''
	统计出现频次最高的 n 个元素
	
	:param items:
	:param n:
	:return:
	'''
	wc = Counter(items)
	return wc.most_common(n)


def do_merge(items1,items2,opt = '+'):
	wc1 = Counter(items1)
	wc2 = Counter(items2)
	wc3 = None
	if opt == '+':
		wc3 = wc1+wc2
	else:
		wc3 = wc1-wc2
	return wc3

if __name__=="__main__":
	try:
		words = [
			'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
			'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
			'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
			'my', 'eyes', "you're", 'under'
			]
		
		print(get_most(words,3)) # [('eyes', 8), ('the', 5), ('look', 4)]
		print(get_times(words,'eyes')) # 如果不存在返回 0
		
		print(cal_wc(words,'eyes'))
		
		wc = do_merge(words,words,opt='+') # 合并counter Counter({'eyes': 16, 'the': 10, 'look': 8, 'into': 6, 'my': 6, 'around': 4, 'not': 2, "don't": 2, "you're": 2, 'under': 2})
		print(wc)
		
		wc = do_merge(words,words,opt='-') # 取差集 Counter()
		print(wc)
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
