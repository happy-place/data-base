#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/6'
Info:
        
"""
print("I'm fib")

def fib(n):
	if n < 2:
		return 1
	else:
		return fib(n-1) + fib(n-2)