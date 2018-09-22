#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/19'
Info:
        
"""
import os,traceback
from collections import namedtuple

def test_namedtuple():
	Subscriber = namedtuple('Subscriber',['addr','joined']) #创建了名为Subscriber的类实例，具备addr，joined两个属性
	sub = Subscriber('tom@cmcm.com','2017-12-12') # 对类实例进行赋值
	print(sub) # Subscriber(addr='tom@cmcm.com', joined='2017-12-12')
	print(sub.addr) # tom@cmcm.com
	
	print(len(sub)) # 集合长度
	
	addr,joined = sub # 解封
	print(addr,joined)


def get_cost(rec_list):
	Stock = namedtuple("Stock",['name','share','price'])
	total = 0.0
	
	for rec in rec_list:
		s = Stock(*rec) # 将所有数据解封
		total += s.share+s.price
	
	print(total)

def do_replace():
	Stock = namedtuple("Stock",['name','share','price'])
	s = Stock('aa',12.3,23)
	ss = s._replace(share = 34) # 创建新对象
	print(s,ss) # Stock(name='aa', share=12.3, price=23) Stock(name='aa', share=34, price=23)

def create_from_dict(a):
	'''
	从dict 构建tuple对象
	:param a:
	:return:
	'''
	Stock = namedtuple('Stock',['name','shares','price','date','time'])
	stock_prototype = Stock('',0,0.0,None,None)
	print(stock_prototype._replace(**a)) # Stock(name='AA', shares=12, price=12.3, date='2018-12-12', time='12:30:30')
	


if __name__=="__main__":
	try:
		'''
		nametuple 可以快速定义一个类模板，并将集合映射到类指定的属性上
		'''
		test_namedtuple()
		
		get_cost([['AA',12.3,23],['BB',12.3,23],['CC',12.3,23]]) # 105.89999999999999
		
		do_replace()
		create_from_dict({'name':'AA','shares':12,'price':12.3,'date':'2018-12-12','time':'12:30:30'})
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)