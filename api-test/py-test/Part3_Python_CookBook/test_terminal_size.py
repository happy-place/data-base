#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

if __name__=="__main__":
	try:
		# 交互式命令行调用时可行的
		sz = os.get_terminal_size()
		print(sz,sz.columns,sz.lines)
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




