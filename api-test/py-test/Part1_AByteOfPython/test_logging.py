#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/16'
Info:
        
"""

import sys,os,traceback,logging
from logging.handlers import RotatingFileHandler


def get_logger(file_name,log_dir='cur_dir/',rollup_size='50m',backups = 2,level=logging.INFO,format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s >> : %(message)s'):
	
	log_dir = log_dir.replace('cur_dir',"/".join(os.path.abspath(sys.argv[0]).split("/")[0:-1])+"/")
	
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
	
	logger_name = os.path.join(log_dir,file_name)
	
	logging.basicConfig(level=level, format=format,filename=logger_name,filemode='w')
	
	# 定义一个RotatingFileHandler，最多保留最近的5个日志文件，每个日志文件最大10M=10 * 1024 * 1024
	
	Rthandler = RotatingFileHandler(logger_name, maxBytes=int(rollup_size[:-1]) * 1024 * 1024, backupCount=backups, encoding="utf-8")
	Rthandler.setLevel(level)
	formatter = logging.Formatter(format)
	Rthandler.setFormatter(formatter)
	logging.getLogger('').addHandler(Rthandler)
	
	logging.info("start logging...")
	
	return logging


if __name__=="__main__":
	try:
		logger = get_logger(file_name='test.log')
		
		logger.info("hello")
		logger.debug("hi")
		logger.warn("ok")
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
	