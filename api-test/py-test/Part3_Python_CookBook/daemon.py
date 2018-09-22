#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/18'
Info:
        
"""
import os
import sys

import atexit
import signal

def daemonize(pidfile, *, stdin='/dev/null',
              stdout='/dev/null',
              stderr='/dev/null'):
	
	# 已经存在的话就直接异常退出
	if os.path.exists(pidfile):
		raise RuntimeError('Already running')
	
	# First fork (detaches from parent) 抓取子进程，返回0表示成功抓取，否则抓取失败，异常退出
	try:
		if os.fork() > 0:
			raise SystemExit(0)   # Parent exit
	except OSError as e:
		raise RuntimeError('fork #1 failed.') # 抓取过程异常退出
	
	os.chdir('/') # 修改子进程工作目录
	os.umask(0) # 修改子进程掩码
	os.setsid() # 重置子进程id
	# Second fork (relinquish session leadership) 第二次抓取子进程
	try:
		if os.fork() > 0:
			raise SystemExit(0)
	except OSError as e:
		raise RuntimeError('fork #2 failed.')
	
	# Flush I/O buffers
	sys.stdout.flush() # 清空标准输出流
	sys.stderr.flush() # 清空标准错误流
	
	# Replace file descriptors for stdin, stdout, and stderr，用自定义的文件描述符 替换 现有的
	with open(stdin, 'rb', 0) as f:
		os.dup2(f.fileno(), sys.stdin.fileno()) #  sys.stdin.fileno() -》f.fileno()
	with open(stdout, 'ab', 0) as f:
		os.dup2(f.fileno(), sys.stdout.fileno())
	with open(stderr, 'ab', 0) as f:
		os.dup2(f.fileno(), sys.stderr.fileno())
	
	# Write the PID file 将当前进程的 pid 拷贝给指定文件
	with open(pidfile,'w') as f:
		print(os.getpid(),file=f)
	
	# Arrange to have the PID file removed on exit/signal 注册新pid 文件
	atexit.register(lambda: os.remove(pidfile))
	
	# Signal handler for termination (required) 注册进程终止时的关机函数
	def sigterm_handler(signo, frame):
		raise SystemExit(1)
	
	signal.signal(signal.SIGTERM, sigterm_handler) # 挂停机钩子

def main():
	import time
	sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
	while True:
		sys.stdout.write('Daemon Alive! {}\n'.format(time.ctime())) # 周期性打印进程消息，此处模拟进程业务
		time.sleep(10)

if __name__ == '__main__':
	PIDFILE = '/tmp/daemon.pid'
	
	if len(sys.argv) != 2:
		print('Usage: {} [start|stop]'.format(sys.argv[0]), file=sys.stderr)
		raise SystemExit(1)
	
	if sys.argv[1] == 'start':
		try:
			daemonize(PIDFILE,
			          stdout='/tmp/daemon.log',
			          stderr='/tmp/dameon.log')
		except RuntimeError as e:
			print(e, file=sys.stderr)
			raise SystemExit(1)
		
		main()
	
	elif sys.argv[1] == 'stop':
		if os.path.exists(PIDFILE):
			with open(PIDFILE) as f:
				os.kill(int(f.read()), signal.SIGTERM)
		else:
			print('Not running', file=sys.stderr)
			raise SystemExit(1)
	
	else:
		print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
		raise SystemExit(1)