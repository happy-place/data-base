#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

def test_exec():
	a = 13
	exec('a=13;print(a+1)') # exec 执行一系列操作
	b = eval('a+1') # eval 执行操作，并将最后一行表达式作为返回值返回
	print(b)

	loc = locals()
	exec('c = a+1') # 通过 locals 获取  exec 作用域中的变量c
	c = loc['c'] # 将locals中局部变量抓回，并重新赋值给 本地变量 c
	print(c)

def test_locals():
	x = 0
	loc = locals()
	print('before: ',loc) # before:  {'x': 0}
	exec('x += 1;print(loc)') # {'x': 1, 'loc': {...}}
	print('after: ',loc) # after:  {'x': 1, 'loc': {...}}
	print('x = ',x,loc['x']) # x =  0 1
 
def test4():
	a = 13
	# ----  直接使用 exec(express) 能够直接从上下文解析 a，然后从locals 局部环境变量获取 b
	loc = locals()
	exec('b=a+1')
	b = loc['b']
	print(b) # 14
	
	# ---- 强制声明使用 loc 自定义本地变量字典 ,glb 回传环境变量字典 exec(express,glb,loc) express 的环境变量到 loc 中获取
	a = 13
	loc = {'a':a}
	glb = {}
	exec('b=a+1',glb,loc) #
	b = loc['b']
	print(glb)
	print(b)





if __name__=="__main__":
	try:
		# test_exec()
		# test_locals()
		test4()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




