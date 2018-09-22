#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/18'
Info:
        
"""
import logging

log = logging.getLogger(__name__) # __name__ 当前模块名称,模块唯一，因此任何调用方创建的 logger 也是唯一的
log.addHandler(logging.NullHandler())
'''
log.addHandler(logging.NullHandler()) 操作将一个空处理器绑定到刚刚已经创建好的logger对象上。
一个空处理器默认会忽略调用所有的日志消息。 因此，如果使用该函数库的时候还没有配置日志，那么将不会有消息或警告出现。
'''

def func():
	log.critical('A Critical Error!')
	log.debug('A Debug message!')




