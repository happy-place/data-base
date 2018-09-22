#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/7'
Info:
        
"""

import os,traceback
from urllib import request


def rest_client():
	url1 = 'http://localhost:8080/hello?name=Tom'
	url2 = 'http://localhost:8080/localtime'
	
	for url in [url1,url2]:
		u = request.urlopen(url)
		print(u.read().decode('utf-8'))
		u.close()
	

if __name__=="__main__":
	try:
		rest_client()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)





