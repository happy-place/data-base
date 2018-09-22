#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,pprint,time
from urllib.request import urlopen,URLError
from socket import timeout

# 一次性捕捉多个
def mix_exp():
	try:
		urlopen('http://www.python.org')
	except (URLError,ValueError,timeout):
		traceback.print_exc()

# 分层捕捉多个
def layer_exp():
	try:
		urlopen('http://www.python.org')
	except URLError as e1:
		print(e1.errno)
	except ValueError as e2:
		print(e2.errno)
	except:
		traceback.print_exc()

def log(msg,target):
	print('{} {!r}'.format(msg,target))

def catch_all():
	try:
		# time.sleep(3)
		
		# raise SystemExit(11)
		# raise KeyboardInterrupt(11)
		raise GeneratorExit(11)
		pass
	except Exception as e1: # 捕捉 SystemExit,KeyboardInterrupt,GeneratorExit 之外异常
		log('Reason1',e1)
	except BaseException as e2: # 捕捉全部异常
		log('Reason2',e2)





if __name__=="__main__":
	try:
		pprint.pprint(FileNotFoundError.__mro__)
		'''
		一下向下追溯到基类 object
		(<class 'FileNotFoundError'>,
		 <class 'OSError'>,
		 <class 'Exception'>,
		 <class 'BaseException'>,
		 <class 'object'>)
		'''
		
		catch_all()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




