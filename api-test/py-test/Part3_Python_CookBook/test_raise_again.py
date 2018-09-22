#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
这个问题通常是当你需要在捕获异常后执行某个操作（比如记录日志、清理等），但是之后想将异常传播下去。
        
"""
import os,traceback

def test_cause():
	try:
		int('N/A')
	except Exception as e:
		print('Exp occure')
		raise # 直接重新抛出异常




if __name__=="__main__":
	try:
		test_cause()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




