#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/17'
Info:
        
"""
import os,traceback


if __name__=="__main__":
	
	try:
		# 系统内置函数 __xx__(self)
		# __init__(self,..) 初始化构造器
	
		# __del__(self) 执行 del xxx 对象被销毁前调用
		
		# __str__(self) 执行 print() 打印时调用
		
		# __lt__(self,other) less than <
		
		# __getitem__(self,key) 根据索引取元素时调用 x[key]
		
		# __len__(self) 对集合元素执行 len() 取长度时调用
		
		# 自定义 private 函数 __xx()
		# __get_data()
		pass
	
	
	
	except:
		traceback.print_exc()
	finally:
		os._exit(0)