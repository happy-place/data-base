#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:

在开发过程中测试HTTP客户端代码常常是很令人沮丧的，因为所有棘手的细节问题都需要考虑（例如cookies、认证、HTTP头、编码方式等）。
要完成这些任务，考虑使用httpbin服务（http://httpbin.org）。这个站点会接收发出的请求，然后以JSON的形式将相应信息回传回来
        
"""
import os,traceback
import requests
from urllib import request,parse
from http.client import HTTPConnection


def get_request():
	# get 请求
	url = 'http://httpbin.org/get'
	params = {
		'name1': 'value1',
		'name2': 'value2'
		}
	
	querystring = parse.urlencode(params)
	
	u = request.urlopen(url+'?'+querystring)
	resp = u.read() # 以json格式返回请求信息
	print(resp)
	'''
	b'{\n
		"args": {\n    "name1": "value1", \n    "name2": "value2"\n  }, \n
	    "headers": {\n    "Accept-Encoding": "identity", \n    "Connection": "close", \n    "Host": "httpbin.org", \n    "User-Agent": "Python-urllib/3.6"\n  },\n
	    "origin": "103.69.155.91", \n
	    "url": "http://httpbin.org/get?name1=value1&name2=value2"\n
	}\n'
	'''
	u.close()
	

def post_request():
	# post 请求
	url = 'http://httpbin.org/post'
	parms = {
		'name1': 'value1',
		'name2': 'value2'
		}
	
	querystring = parse.urlencode(parms)
	u = request.urlopen(url,querystring.encode('ascii'))
	resp = u.read()
	print(resp)
	'''
	b'{\n
		"args": {}, \n
		"data": "", \n
		"files": {}, \n
		"form": {\n    "name1": "value1", \n    "name2": "value2"\n  }, \n
		"headers": {\n    "Accept-Encoding": "identity", \n    "Connection": "close", \n    "Content-Length": "25", \n    "Content-Type": "application/x-www-form-urlencoded", \n    "Host": "httpbin.org", \n    "User-Agent": "Python-urllib/3.6"\n  }, \n
		"json": null, \n
		"origin": "103.69.155.91", \n
		"url": "http://httpbin.org/post"\n
	}\n'

	'''
	u.close


def my_header():
	# 修改http 请求头
	url = 'http://httpbin.org/post'
	
	headers = {
		'User-agent': 'none/ofyourbusiness',
		'Spam': 'Eggs'
		}
	
	parms = {
		'name1': 'value1',
		'name2': 'value2'
		}
	
	querystring = parse.urlencode(parms)
	
	req = request.Request(url, querystring.encode('ascii'),headers = headers)
	
	u = request.urlopen(req)
	resp = u.read()
	print(resp)
	'''
	b'{\n
		"args": {}, \n
		"data": "", \n
		"files": {}, \n
		"form": {\n    "name1": "value1", \n    "name2": "value2"\n  }, \n
		"headers": {\n    "Accept-Encoding": "identity", \n    "Connection": "close", \n    "Content-Length": "25", \n    "Content-Type": "application/x-www-form-urlencoded", \n    "Host": "httpbin.org", \n    "Spam": "Eggs", \n    "User-Agent": "none/ofyourbusiness"\n  }, \n
		"json": null, \n
		"origin": "103.69.155.91", \n
		"url": "http://httpbin.org/post"\n
	}\n'

	'''
	u.close()
	

def complex_req():
	# 更为复杂请求使用 requests 模块
	url = 'http://httpbin.org/post'
	
	headers = {
		'User-agent': 'none/ofyourbusiness',
		'Spam': 'Eggs'
		}
	
	parms = {
		'name1': 'value1',
		'name2': 'value2'
		}
	
	resp = requests.post(url,data=parms,headers=headers)
	text = resp.text
	bintext = resp.content
	jsontext = resp.json()
	
	print(text)
	'''
	{
	  "args": {},
	  "data": "",
	  "files": {},
	  "form": {
	    "name1": "value1",
	    "name2": "value2"
	  },
	  "headers": {
	    "Accept": "*/*",
	    "Accept-Encoding": "gzip, deflate",
	    "Connection": "close",
	    "Content-Length": "25",
	    "Content-Type": "application/x-www-form-urlencoded",
	    "Host": "httpbin.org",
	    "Spam": "Eggs",
	    "User-Agent": "none/ofyourbusiness"
	  },
	  "json": null,
	  "origin": "103.69.155.91",
	  "url": "http://httpbin.org/post"
	}
	
	'''
	
	print(bintext) # 二进制编码
	'''
	b'{\n
		"args": {}, \n
		"data": "", \n
		"files": {}, \n
		"form": {\n    "name1": "value1", \n    "name2": "value2"\n  }, \n
		"headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "gzip, deflate", \n    "Connection": "close", \n    "Content-Length": "25", \n    "Content-Type": "application/x-www-form-urlencoded", \n    "Host": "httpbin.org", \n    "Spam": "Eggs", \n    "User-Agent": "none/ofyourbusiness"\n  }, \n
		"json": null, \n  "origin": "103.69.155.91", \n
		"url": "http://httpbin.org/post"\n
	}\n'

	'''
	
	print(jsontext) # json 格式请求
	'''
	{
		'args': {},
		'data': '',
		'files': {},
		'form': {'name1': 'value1', 'name2': 'value2'},
		'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Content-Length': '25', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'httpbin.org', 'Spam': 'Eggs', 'User-Agent': 'none/ofyourbusiness'},
		'json': None,
		'origin': '103.69.155.91',
		'url': 'http://httpbin.org/post'
	}
	'''
	
def head_req():
	# 请求页面头部信息
	resp = requests.head('https://www.python.org/')

	status = resp.status_code
	headers = resp.headers
	
	print(status)
	print(headers)
	'''
	{'Server': 'nginx', 'Content-Type': 'text/html; charset=utf-8', 'X-Frame-Options': 'SAMEORIGIN', 'x-xss-protection': '1; mode=block', 'X-Clacks-Overhead': 'GNU Terry Pratchett', 'Via': '1.1 varnish, 1.1 varnish', 'Content-Length': '48825', 'Accept-Ranges': 'bytes', 'Date': 'Tue, 07 Aug 2018 00:17:49 GMT', 'Age': '2103', 'Connection': 'keep-alive', 'X-Served-By': 'cache-iad2135-IAD, cache-hkg17924-HKG', 'X-Cache': 'HIT, HIT', 'X-Cache-Hits': '5, 2', 'X-Timer': 'S1533601069.125049,VS0,VE3', 'Vary': 'Cookie', 'Strict-Transport-Security': 'max-age=63072000; includeSubDomains'}
	'''

def req_with_auth():
	# 带认证授权请求
	resp = requests.get('http://pypi.python.org/pypi?:action=login',auth=('user','password'))
	status_code = resp.status_code
	info = resp.text
	print(status_code) # 200
	print(info)
	'''
	<!DOCTYPE html>
		<html lang="en">
		  <head>
		    <meta charset="utf-8">
		    <meta http-equiv="X-UA-Compatible" content="IE=edge">
		    <meta name="viewport" content="width=device-width, initial-scale=1">
		    <meta name="defaultLanguage" content="en">
		    <meta name="availableLanguages" content="en">
		    ....
	'''


def pass_cookie():
	# 多次请求间传递 cookie
	url = 'http://pypi.python.org/pypi?:action=login'
	auth=('user','password')
	
	resp1 = requests.get(url,auth=auth)
	print(resp1.cookies) # <RequestsCookieJar[]>
	
	resp2 = requests.get(url, cookies = resp1.cookies)
	print(	resp2.cookies)


def do_upload():
	# 上传 csv 文件
	url = 'http://httpbin.org/post'
	files = {'file': ('stocks.csv',open('stocks.csv','rb'))}
	resp = requests.post(url,files=files)
	info = resp.text
	print(info)
	'''
	{
	  "args": {},
	  "data": "",
	  "files": {
	    "file": "Symbol,Price,Date,Time,Change,Volume\n\"AA\",39.48,\"6/11/2007\",\"9:36am\",-0.18,181800\n\"AIG\",71.38,\"6/11/2007\",\"9:36am\",-0.15,195500\n\"AXP\",62.58,\"6/11/2007\",\"9:36am\",-0.46,935000\n\"BA\",98.31,\"6/11/2007\",\"9:36am\",+0.12,104800\n\"C\",53.08,\"6/11/2007\",\"9:36am\",-0.25,360900\n\"CAT\",78.29,\"6/11/2007\",\"9:36am\",-0.23,225400"
	  },
	  "form": {},
	  "headers": {
	    "Accept": "*/*",
	    "Accept-Encoding": "gzip, deflate",
	    "Connection": "close",
	    "Content-Length": "454",
	    "Content-Type": "multipart/form-data; boundary=a7bfd0167ecd8191dd842f3d16cb59b0",
	    "Host": "httpbin.org",
	    "User-Agent": "python-requests/2.19.1"
	  },
	  "json": null,
	  "origin": "103.69.155.91",
	  "url": "http://httpbin.org/post"
	}
	'''
	resp.close()

def req_by_http_client():
	# 不使用第三方库 requests 条件下，直接视图底层 http.client 模块发送复杂请求
	c = HTTPConnection('www.python.org',80)
	c.request('HEAD','index.html')
	resp = c.getresponse()
	print('Status',resp.status) # Status 301
	
	for name,value in resp.getheaders():
		print(name,value)
	'''
	Server Varnish
	Retry-After 0
	Location https://www.python.orgindex.html
	Content-Length 0
	Accept-Ranges bytes
	Date Tue, 07 Aug 2018 00:39:13 GMT
	Via 1.1 varnish
	Connection close
	X-Served-By cache-hkg17923-HKG
	X-Cache HIT
	X-Cache-Hits 0
	X-Timer S1533602354.741277,VS0,VE0
	Strict-Transport-Security max-age=63072000; includeSubDomains
	'''

def req_with_auth_by_urllib():
	auth = request.HTTPBasicAuthHandler()
	auth.add_password('pypi','http://pypi.python.org','username','password')
	opener = request.build_opener(auth)
	
	r = request.Request('http://pypi.python.org/pypi?:action=login')
	u = opener.open(r)
	resp = u.read()
	print(resp)
	'''
	b'\n\n\n\n\n\n<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="utf-8">\n
	'''







if __name__=="__main__":
	try:
		# get_request()
		# post_request()
		# my_header()
		# complex_req()
		# head_req()
		# req_with_auth()
		# pass_cookie()
		do_upload()
		# req_by_http_client()
		# req_with_auth_by_urllib()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




