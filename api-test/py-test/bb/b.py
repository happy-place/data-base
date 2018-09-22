#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/23'
Info:
        
"""

import os, sys

from aa.a import *

print(os.getcwd())

if __name__=="__main__":
	try:
		sayhi()
	finally:
		os._exit(0)