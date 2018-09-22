#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/25'
Info:
        
"""

import os,traceback,csv,re
from collections import namedtuple

def read_from_csv():
	with open('stocks.csv','r') as f:
		f_csv = csv.reader(f)
		headers = next(f_csv)
		print(headers)
		for row in f_csv:
			print(row[0],row[1]) # 通过索引访问
			print(row)
			
	'''
	['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
	['AA', '39.48', '6/11/2007', '9:36am', '-0.18', '181800']
	['AIG', '71.38', '6/11/2007', '9:36am', '-0.15', '195500']
	['AXP', '62.58', '6/11/2007', '9:36am', '-0.46', '935000']
	['BA', '98.31', '6/11/2007', '9:36am', '+0.12', '104800']
	['C', '53.08', '6/11/2007', '9:36am', '-0.25', '360900']
	['CAT', '78.29', '6/11/2007', '9:36am', '-0.23', '225400']
	'''
			
	pass

def read_from_csv2():
	with open('stocks.csv','r') as f:
		f_csv = csv.reader(f)
		headers = next(f_csv)
		print(headers)
		
		Row = namedtuple('Row',headers) # 快速定义类模板
		
		for row in f_csv:
			row = Row(*row)
			print(row.Symbol,row.Price,row.Date) # CAT 78.29 6/11/2007 # 通过属性字段进行访问
			print(row) # Row(Symbol='CAT', Price='78.29', Date='6/11/2007', Time='9:36am', Change='-0.23', Volume='225400')
			
	pass

def read_from_csv3():
	# 直接通过列名访问元素
	with open('stocks.csv','r') as f:
		f_csv = csv.DictReader(f)
		for row in f_csv:
			print(row['Symbol'],row['Price'])
		
	pass



def test_write_2_csv():
	headers = ['Symbol','Price','Date','Time','Change','Volume']
	rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
        ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
        ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
        ]
	
	with open('stocks2.csv','w') as f:
		f_csv = csv.writer(f) # 通 csv 模块包装普通文件流
		f_csv.writerow(headers) # 写列头
		f_csv.writerows(rows) # 写列
		f.flush() # 刷出

def test_write_2_csv2():
	headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
	rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
         'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
        {'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
         'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
        {'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
         'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
        ]
	
	with open('stocks3.csv','w') as f:
		f_csv = csv.DictWriter(f,headers)  # 包装流过程中就将表头封装在内了
		f_csv.writeheader()
		f_csv.writerows(rows)


def read_from_tsv():
	# 直接通过列名访问元素
	with open('stocks.tsv','r') as f:
		f_csv = csv.reader(f,delimiter = '\t') # \t 分割
		for row in f_csv:
			print(row)
	
	pass

def test_write_2_tsv():
	headers = ['Symbol','Price','Date','Time','Change','Volume']
	rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
	        ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
	        ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
	        ]
	
	with open('stocks.tsv','w') as f:
		f_csv = csv.writer(f,delimiter = '\t') # 通 csv 模块包装普通文件流
		f_csv.writerow(headers) # 写列头
		f_csv.writerows(rows) # 写列
		f.flush() # 刷出

def test_clean():
	with open('stocks_clean.csv') as f:
		f_csv = csv.reader(f)
		
		headers = [ re.sub('[^a-zA-Z_,]', '_', h) for h in next(f_csv) ] # 将列名中的空格使用下划线补全'CN Symbol' -> 'CN_Symbol'
	
		Row = namedtuple('Row',headers)
		for r in f_csv:
			row = Row(*r)
			print(row)
		'''
		Row(CN_Symbol='AA', Max_Price='39.48', Last_Date='6/11/2007', Cur_Time='9:36am', Change='-0.18', Volume='181800')
		'''

def do_convert():
	col_type = [str,float,str,str,float,int]
	with open('stocks.csv') as f:
		f_csv = csv.reader(f)
		headers = next(f_csv)
		Row = namedtuple('Row',headers)
		for row in f_csv:
			# tuple() 中传入生成器，实现类型强转
			row = tuple(convert(value) for convert,value in zip(col_type,row))
			row = Row(*row)
			print(row)
	'''
	Row(Symbol='AA', Price=39.48, Date='6/11/2007', Time='9:36am', Change=-0.18, Volume=181800)
	'''

def do_convert2():
	'''
	局部字段强转
	:return:
	'''
	col_type = [str,float,str,str,float,int]
	field_type = [('Price',float),('Change',float),('Volume',int)]

	with open('stocks.csv') as f:
		f_csv = csv.DictReader(f)
		for row in f_csv:
			row.update((k,v(row[k])) for k,v in field_type)
			print(row['Symbol']) # BA
			print(row) # OrderedDict([('Symbol', 'AXP'), ('Price', 62.58), ('Date', '6/11/2007'), ('Time', '9:36am'), ('Change', -0.46), ('Volume', 935000)])
		
		
		

if __name__=="__main__":
	try:
		# read_from_csv()
		# read_from_csv2()
		# read_from_csv3()
		# test_write_2_csv()
		# test_write_2_csv2()
		# test_write_2_tsv
		# read_from_tsv()
		# test_clean()
		# do_convert()
		do_convert2()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




