#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/17'
Info:
        
"""

import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')



# 脚本编译乱码： 第二行 # -*- coding: utf-8 -*- 明确脚本编码，如果不写，默认为 ascii 编码，页面出现 中文会报错 'SyntaxError: Non-ASCII character '\xe3' in file'

# print 打印字符输出呈现 unicode 编码问题，在python2.7 环境通过设置 reload(sys) 和 sys.setdefaultencoding('utf-8') 可正常显示中文
