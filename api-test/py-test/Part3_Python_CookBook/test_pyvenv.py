#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        创建虚拟环境
        huhao:~ huhao$ cd /Users/huhao/Desktop/
        huhao:Desktop huhao$ pyvenv Spam
        huhao:Desktop huhao$ cd Spam/
		huhao:Spam huhao$ ls ./
		bin             include         lib             pyvenv.cfg
        Python 3.6.5 (default, Mar 30 2018, 06:42:10)
		[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)] on darwin
		Type "help", "copyright", "credits" or "license" for more information.
		>>> from pprint import pprint
		>>> import sys
		>>> pprint(sys.path)
		['',
		 '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python36.zip',
		 '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6',
		 '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/lib-dynload',
		 '/Users/huhao/Desktop/Spam/lib/python3.6/site-packages']
		>>>
		
		默认情况下，虚拟环境是空的，不包含任何额外的第三方库。如果你想将一个已经安装的包作为虚拟环境的一部分，
		可以使用“–system-site-packages”选项来创建虚拟环境，
        pyvenv --system-site-packages Spam
        
"""

import os,traceback

if __name__=="__main__":
	try:
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




