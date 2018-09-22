#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:


1).创建如下目录结构

projectname/
	MANIFEST.in
	setup.py
    README.txt
    Doc/
        documentation.txt
    projectname/
        __init__.py
        foo.py
        bar.py
        utils/
            __init__.py
            spam.py
            grok.py
    examples/
        helloworld.py

2).编辑顶层文件
# setup.py
from distutils.core import setup

setup(name='projectname',
    version='1.0',
    author='Your Name',
    author_email='you@youraddress.com',
    url='http://www.you.com/projectname',
    packages=['projectname', 'projectname.utils'],
)

# MANIFEST.in
include *.txt
recursive-include examples *
recursive-include Doc *

3).执行打包命令
cd projectname 进入顶层目录
python3 setup.py sdist 执行打包
注：此时顶层目录下会新生成 dist/projectname-1.0.zip 或 projectname-1.0.tar.gz 文件 和 MANIFEST 文件












"""
import os,traceback

if __name__=="__main__":
	try:
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




