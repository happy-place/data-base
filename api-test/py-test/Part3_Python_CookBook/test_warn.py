#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,warnings

def func(x,y,logfile=None,debug=False):
	if logfile is not None:
		warnings.warn('logfile argument deprecated',DeprecationWarning) # 相当于抛出DeprecationWarning异常

def test_always():
	# 设置 警告模式
	warnings.simplefilter('always')
	# 直接删除未关闭的流对象，出现如下警告信息 ResourceWarning: unclosed file <_io.TextIOWrapper name='app.log' mode='r' encoding='UTF-8'>
	f = open('app.log')
	del f



if __name__=="__main__":
	try:
		# func(1,2,'aa.txt')
		'''
		python3 -W all test_warn.py 显示全部警告
		python3 -W ignore test_warn.py 忽略全部警告
		python3 -W error test_warn.py 有警告处，直接运行报错
		python3 -W always test_warn.py 等同于 all
		
		python3 -W all test_warn.py
		test_warn.py:14: DeprecationWarning: logfile argument deprecated
        warnings.warn('logfile argument deprecated',DeprecationWarning) # 相当于抛出DeprecationWarning异常
		'''
		
		test_always()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




