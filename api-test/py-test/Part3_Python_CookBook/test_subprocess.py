#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,subprocess,shlex


def get_netstate(*cmd):
	try:
		# ['cmd','arg1','arg2'] # 默认情况直接返回正确输出信息，需要收集错误信息 使用 stderr=subprocess.STDOUT
		# 超时使用 subprocess.TimeExpired 处理异常
		# 负责命令需要传给 shell 执行使用 shell=True
		out_bytes = subprocess.check_output(cmd,stderr=subprocess.STDOUT,timeout=2)
		
		print(out_bytes.decode('utf-8'))
	except subprocess.CalledProcessError as e: # 执行指令失败，返回错误信息和状态码
		out_bytes = e.output.decode('utf-8')
		code = e.returncode
		print(out_bytes,code)
	'''
	total 153800
	-rw-r--r--   1 huhao  staff       371  7 27 14:31 Part3_Python_CookBook.iml
	drwxr-xr-x   2 huhao  staff        68  7 25 09:58 aa
	-rw-r--r--   1 huhao  staff        16  7 23 13:57 array.txt
	-rw-r--r--   1 huhao  staff        22  7 23 12:50 byte.txt
	-rw-r--r--   1 huhao  staff        32  7 25 11:36 cnt.txt
	'''

def test_complex_cmd(ars):
	try:
		ars = shlex.quote(ars) # 引用参数
		out_bytes = subprocess.check_output('echo {ars} | wc > /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/wc.txt'.format(ars=ars),
		                                    shell=True)
		
		
		print(out_bytes.decode('utf-8')) #   1       1      11 一行 一个单词，11个字节
	except subprocess.CalledProcessError as e: # 执行指令失败，返回错误信息和状态码
		out_bytes = e.output.decode('utf-8')
		code = e.returncode
		print(out_bytes,code)

def test_popen():
	text = b'''
	hello world
	this is a test
	goodbye
	'''
	# 执行复杂交互指令，返回获取信息 或 错误信息
	p = subprocess.Popen(['ls'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
	
	stdout,stderr = p.communicate(text)
	
	if stdout :
		print(stdout.decode('utf-8')) #        4       7      40
		
	if stderr:
		print(stderr.decode('utf-8'))


if __name__=="__main__":
	try:
		# get_netstate('ls','-l')
		# get_netstate('ls','-l4') # stderr
		# get_netstate('netstat','-a') # timeout
		# test_complex_cmd('helloworld')
		
		test_popen()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




