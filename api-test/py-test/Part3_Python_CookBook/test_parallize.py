#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
import gzip,io,glob
from concurrent import futures

def find_robots(filename):
	robots = set()
	with gzip.open(filename) as f:
		# 解码，并检测
		for line in io.TextIOWrapper(f,encoding='ascii'):
			fields = line.split()
			if fields[6] == '/robots.txt':
				robots.add(fields[0]) # 抓取ip
	return robots


def find_all_robots(logdir):
	# 正则查找匹配的文件列表
	files = glob.glob(logdir+'/*.log.gz')
	all_robots = set()
	for robots in map(find_robots,files):
		all_robots.update(robots)
	return all_robots


def pariallize_find_all(logdir):
	# 正则查找匹配的文件列表
	files = glob.glob(logdir+'/*.log.gz')
	all_robots = set()
	# 创建与系统核数相同格式的线程并行解析
	with futures.ProcessPoolExecutor() as pool:
		for robots in pool.map(find_robots,files):
			all_robots.update(robots)
	return all_robots
	
	
	for robots in map(find_robots,files):
		all_robots.update(robots)
	return all_robots

def add(x,y):
	return x + y

def when_done(r):
	print('Got: ',r.result())

def test_callback():
	with futures.ProcessPoolExecutor() as pool:
		future_result = pool.submit(add, 1,2)
		# 执行完毕自动回调
		future_result.add_done_callback(when_done)


def test_find():
	robots = find_all_robots('logs')
	for ipaddr in robots:
		print(ipaddr)
	

if __name__=="__main__":
	try:
		test_callback()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




