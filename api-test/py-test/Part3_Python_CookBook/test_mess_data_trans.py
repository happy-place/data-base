#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback

def send_from(arr, dest):
	view = memoryview(arr).cast('B')
	while len(view):
		nsent = dest.send(view)
		view = view[nsent:]

def recv_into(arr, source):
	view = memoryview(arr).cast('B')
	while len(view):
		nrecv = source.recv_into(view)
		view = view[nrecv:]

__all__ = ['send_from','recv_into']




