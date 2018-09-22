#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/16'
Info:
        
"""
import os


if __name__=="__main__":
	try:
		with open("/Users/huhao/Desktop/aa/1.txt",'rb') as f:
			lines = f.readlines()
			print(lines)
			f.close()
		
		with open("/Users/huhao/Desktop/aa/2.txt",'wb') as f:
			lines = [x.upper() for x in lines]
			f.writelines(lines)
			f.flush()
			f.close()
	
	finally:
		os._exit(0)

