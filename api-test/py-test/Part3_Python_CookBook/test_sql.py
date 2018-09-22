#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/25'
Info:
        
"""
import os,traceback,sqlite3


def test_sqlite3():
	try:
		# 连接默认库
		db = sqlite3.connect('database.db')
		# 创建游标
		cursor = db.cursor()
		# 建表
		cursor.execute('create table portfolio (symbol text,shares integer,price real)')
		# 手动提交
		db.commit()
		
		stocks = [
			('GOOG', 100, 490.1),
			('AAPL', 50, 545.75),
			('FB', 150, 7.45),
			('HPQ', 75, 33.2),
			]
		
		# 插入数据
		cursor.executemany("insert into portfolio values (?,?,?)",stocks )
		db.commit()
		
		# 查询
		for row in db.execute('select * from portfolio'):
			print(row)
			
	finally:
		# 关闭资源
		cursor.close()
		db.close()

def test_select():
	try:
		# 连接默认库
		db = sqlite3.connect('database.db') # 在相同路径先创建了 database.db 文件
		# 创建游标
		cursor = db.cursor()
		
		# 传入占位符? ,进行条件查询
		for row in db.execute('select * from portfolio where price > ?',(500.0,)):
			print(row)
	
	finally:
		# 关闭资源
		cursor.close()
		db.close()



if __name__=="__main__":
	try:
		# test_sqlite3()
		test_select()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
		
		
		
		