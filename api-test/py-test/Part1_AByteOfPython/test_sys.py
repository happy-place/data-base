#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/16'
Info:
        
"""
import sys,os,traceback,json,urllib,urllib.parse,urllib.request,urllib.response

class YahooSearchError(Exception):
	pass

def get_version_info():
	ver_list = sys.version_info
	# sys.version_info(major=3, minor=6, micro=5, releaselevel='final', serial=0) 3 版本信息
	print(ver_list,ver_list[0])
	
	print(sys.platform)
	
	return ver_list[0]


def fetch_data(query,results=20,start=1,**kwargs):
	YAHOO_APP_ID = 'jl22psvV34HELWhdfUJbfDQzlJ2B57KFS_qs4I8D0Wz5U5_yCI1Awv8.lBSfPhwr'
	SEARCH_BASE = 'http://search.yahooapis.com/WebSearchService/V1/webSearch'
	
	kwargs.update({
		'appid': YAHOO_APP_ID,
		'query': query,
		'results': results,
		'start': start,
		'start': start,
		'output': 'json'
		})
	
	url = SEARCH_BASE+ "?" + urllib.parse.urlencode(kwargs) # 使用 urllib.parse 模块对 kv 请求参数 对进行编码
	result = json.load(urllib.request.urlopen(url)) # load 从流获取 json,loads 从str 获取json
	
	if 'Error' in result:
		raise YahooSearchError(result['Error'])
	
	return result['ResultSet']
	


if __name__=="__main__":
	try:
		if get_version_info() !=3:
			sys.exit("This program needs Python 3.0")  # 强制在 3.0 版本运行，出栈，但虚拟机不会关闭
		
		query = input('What do you want to search for?')
		
		for result in fetch_data(query)['Result']:
			print('{title}: {url}'.format(title=result['Title'],url=result['Url']))
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)  # 关闭虚拟机
	
	