#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
'''
当 pk1/pk11/__init__.py 中定义了如下语句时，可以直接通过 from pk1 import pk11 ，加载 a1.py, a2.py 到本模块
from . import a1
from . import a2

否则需要使用如下语句才能生效
import pk1.pk11.a1 as a1
import pk1.pk11.a2 as s2

如果 pk1/pk11/a1.py 中定义了 __all__=['hi_a1'] 属性，并且使用 from  pk1.pk11.a1 import * 引入，则 a.py 模块中出 hi_a1 之外的
函数都不能被调用，但通过  import pk1.pk11.a1 as a1 引入时，a1.say_hi()则可成功调用

以相对路径导包
mypackage/
    __init__.py
    A/
        __init__.py
        spam.py
        grok.py
    B/
        __init__.py
        bar.py

# mypackage/A/spam.py
from . import grok

# mypackage/A/spam.py
from ..B import bar


'''
# from pk1 import pk11

from  pk1.pk11.a1 import *




if __name__=="__main__":
	try:
		
		hi_a1()
		# say_hi()
	
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




