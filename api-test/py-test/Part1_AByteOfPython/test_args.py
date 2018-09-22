#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/14'
Info:
        
"""
import sys,os

def do1(a,*li): # 接受list
	print(a)
	print(li)
	
	
def do2(a,**dic): # 接受dict
	print(a)
	print(dic['a'])


def do3(a,b=1,c=2): # 具名传参
	print(a)
	print(b)
	print(c)

def get_tuple():
	return (3,4)


def pow_sum(power,*args):
	'''
	:param power: 幂次
	:param args: 底数集合
	:return:
	'''
	res = 0
	for num in args:
		res += pow(num,power)
	print(res)



if __name__=="__main__":
	try:
		do1(1,2,3,4)
		do1(1,{'a':1,'b':2})
		do3(0,b=2)
		
		a,b = get_tuple() # 传送元祖
		c,*d = [1,2,3,4] # 分拆集合
		
		b,a = a,b # 交换元素
		
		print(a,b,c,d)
		
		pow_sum(2,1,2,3) # pow_sum(power,*args) power= 2, 1,2,3 >> args
		pow_sum(2,*range(1,4)) # *list_elem 会自动解封集合元素
		
	finally:
		os._exit(0)
# sys.exit(0) # 在此处没用