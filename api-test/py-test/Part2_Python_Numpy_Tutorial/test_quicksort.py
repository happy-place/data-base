#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/17'
Info:
        
"""

import sys,os

def quicksort(arr):
	'''
	快排
	:param arr: 带排序集合
	:return:
	'''
	if len(arr) <=1:
		return arr
	pivot = arr[len(arr) // 2]
	left = [x for x in arr if x<pivot]  # 收集比pivot小的元素
	middle = [x for x in arr if x == pivot] # 收集与pivot相等
	right = [x for x in arr if x > pivot] # 收集比pivot大的元素
	return quicksort(left) + middle + quicksort(right) # 递归


if __name__=="__main__":
	try:
		print(quicksort([2,3,1,2,6,7,3,4,5]))
		pass
	
	finally:
		os._exit(0)




