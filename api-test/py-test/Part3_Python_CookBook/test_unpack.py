#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback

def drop_first_last(grades):
	grades.sort() # 排序
	first,*middle,last = grades # 去掉最高最低分
	return sum(middle)/len(middle) # 求平均值

def do_compare(recored):
	'''
	历史平均值与当前值进行对比
	:param recored:
	:return:
	'''
	*before,now = recored
	before_avg = sum(before)/len(before)
	return (before_avg,now)

def sum(items):
	head,*tail =items
	# 如果tail为空返回head 窦泽，返回tail,三元运算，递归累计求和
	return head + sum(tail) if tail else head



if __name__=="__main__":
	try:
		
		# 解封赋值 unpack 每层元素个数必须一致，否则会报错
		x,y = (4,5)
		print(x,y)
		
		name,share,price,(year,month,day) = ['acme',50,91.1,(2018,1,12)]
		print(name,year)
		
		a,b,c = 'ABC' # 字符串属于可迭代对象
		print(a,b,c)
		
		# 局部遮盖
		data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
		_,share,price,_ = data
		print(share,price)
		
		print(drop_first_last([1,2,4,2]))
		
		# 不确定个数的字段放在最后
		nane,email,*phone_nums = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
		print(phone_nums)
		
		print(do_compare([10, 8, 7, 1, 9, 5, 10, 3]))
		
		# 使用 * 收集集合对象
		records = [
			('foo', 1, 2),
			('bar', 'hello'),
			('foo', 3, 4),
			]
		
		for tag ,*args in records:
			if tag == 'foo':
				x,y = args
				print(tag,x,y)
			else:
				x = args[0]
				print(tag,x)
		
		line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
		uname,*fields,homedir,sh = line.split(":") # 字符串分割，解封赋值
		print(uname,homedir,sh)
		
		record = ('ACME', 50, 123.45, (12, 18, 2012))
		name,*_,(*_,year) = record
		print(year)
		
		items = [1,10,7,4,5,9]
		head,*tail = items
		print(head,tail)
		
		print(sum([1,2,3]))
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)

