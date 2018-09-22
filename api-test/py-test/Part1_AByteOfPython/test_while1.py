#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/13'
Info:
        
"""
import sys,os


if __name__=="__main__":
	num=1
	runninrg = True
	while runninrg:
		guess = int(input("please enter a num: "))  # input 函数接受控制台参数
		if guess >num :
			print("{guess} > {num}".format(guess=guess,num=num))
		elif guess<num :
			print("{guess} < {num}".format(guess=guess,num=num))
			if guess == -1:
				break # 终止循环，不会执行else
		else:
			print("{guess} = {num}".format(guess=guess,num=num))
			runninrg = False
	else:
		print("stop")  # while 执行到最后，需要过 else
	
	os._exit(0)
	# sys.exit(0) # 在此处没用
	