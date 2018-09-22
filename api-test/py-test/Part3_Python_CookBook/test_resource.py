#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
import signal,resource

def time_exceeded(signo,frame):
	print(signo) # 24
	print("Time's up!")
	raise SystemExit(1)

def set_max_runtime(seconds):
	soft,hard = resource.getrlimit(resource.RLIMIT_CPU)
	print(soft,hard)
	resource.setrlimit(resource.RLIMIT_CPU,(seconds,hard))
	signal.signal(signal.SIGXCPU,time_exceeded)
	
def limit_memory(maxsize):
	soft,hard = resource.getrlimit(resource.RLIMIT_AS)
	resource.setrlimit(resource.RLIMIT_AS,(maxsize,hard))

if __name__=="__main__":
	try:
		set_max_runtime(3)
		while True:
			pass
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




