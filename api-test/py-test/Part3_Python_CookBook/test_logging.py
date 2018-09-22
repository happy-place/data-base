#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,logging,sys
import logging.config
import somelib

def main():
	logging.basicConfig(filename='app.log',level=logging.WARNING,format='%(levelname)s:%(asctime)s:%(message)s') #
	hostname = 'www.python.org'
	item = 'spam'
	filename='data.csv'
	mode = 'r'
	
	# 降序排列，值大于 >= basicConfig中定义级别的日志
	logging.critical('Host %s unknown',hostname)
	logging.error("Couldn't find %r",item)
	logging.warning('Feature is depreciated')
	logging.info('Opening file %r. mode=%r',filename,mode)
	logging.debug('Got here')
	'''
	CRITICAL:2018-08-18 16:01:25,945:Host www.python.org unknown
	ERROR:2018-08-18 16:01:25,947:Couldn't find 'spam'
	WARNING:2018-08-18 16:01:25,948:Feature is depreciated
	'''

def log_ini():
	# 通过文件配置 logging
	logging.config.fileConfig('logconfig.ini')
	logging.basicConfig(level=logging.ERROR) # 修改日志级别
	logging.warning('Feature is depreciated')
	logging.error("Couldn't find %r",[1,2,3])

# basicConfig() 在程序中只能被执行一次。如果你稍后想改变日志配置， 就需要先获取 root logger ，然后直接修改它。
def get_logger():
	logging.config.fileConfig('logconfig.ini')
	logger = logging.getLogger(sys.argv[0].replace('.py',''))
	logger.level = logging.ERROR
	logger.warning('Feature is depreciated')
	logger.error("Couldn't find %r",[1,2,3])

def test_somelib():
	print('first call')
	somelib.func()
	
	print('second call')
	logging.basicConfig()
	somelib.func()
	'''
	CRITICAL:somelib:A Critical Error!
	'''
	
	print('third call')
	logging.getLogger('somelib').level = logging.DEBUG # 修改日志级别
	somelib.func()
	'''
	CRITICAL:somelib:A Critical Error!
	DEBUG:somelib:A Debug message!
	'''
	
	


if __name__=="__main__":
	try:
		# main()
		# log_ini()
		# get_logger()
		test_somelib()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




