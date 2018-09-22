#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,sys

# 退出程序，并输出错误信息
def test_exit():
	sys.stderr.write('It failed !\n')
	raise SystemExit(1)

if __name__=="__main__":
	try:
		test_exit()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




