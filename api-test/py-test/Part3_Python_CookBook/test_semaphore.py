#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,threading,time


def worker(n,sema):
	sema.acquire()
	print('Working',n)

def start_thread():
	sema = threading.Semaphore(0)
	nworkers = 3
	
	# 同时启动 nworkers 个线程，所有线程遇到 sema.acquire() 发送阻塞，每执行一次 sema.release() 就释放，就按先后顺序释放一次
	for n in range(nworkers):
		t = threading.Thread(target=worker,args=(n,sema,))
		t.start()
	
	sema.release()
	time.sleep(2)
	
	sema.release()
	time.sleep(2)


if __name__=="__main__":
	try:
		start_thread()
		
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




