#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,fileinput


def do_print():
	with fileinput.input() as f_input:
		for line in f_input:
			print(line,end='')

def desc_file():
	# fileinput.input() 自动打开输入文件的流模式
	with fileinput.input() as f_input:
		for line in f_input:
			print(f_input.filename(),f_input.lineno(),line,end='')


if __name__=="__main__":
	try:
		'''
		# python test_fileinput.py /etc/passwd 打印指定文件
		# python test_fileinput.py < /etc/passwd 打印重定向输入的文件
		# echo 'hello' | python3 test_fileinput.py 基于管道接受数据
		# ls | python3 test_fileinput.py
		'''
		# do_print()
		
		desc_file()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




