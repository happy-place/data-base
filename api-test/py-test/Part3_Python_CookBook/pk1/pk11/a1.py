#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/6'
Info:
        
"""

def hi_a1():
	print('hi_a1')

def say_hi():
	print('hi')

# 只允许暴露 hi_a1
__all__ = ['hi_a1']