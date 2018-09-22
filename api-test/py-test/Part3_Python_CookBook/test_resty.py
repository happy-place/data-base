#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/7'
Info:
        
"""

import cgi,time,os,traceback
from wsgiref.simple_server import make_server



class PathDispatcher:
	# 初始化处理器映射字典
	def __init__(self):
		self.pathmap = {}
	
	# 分发请求
	def __call__(self,environ,start_response):
		# 提取请求资源
		path = environ['PATH_INFO']
		# 封装请求参数 wsgi.input -> python obj -> params dict
		params = cgi.FieldStorage(['wsgi.input'],environ = environ)
		# 提取请求方式  GET / POST
		method = environ['REQUEST_METHOD'].lower()
		# 请求参数封装 python obj -> params dict
		environ['params'] = {key: params.getvalue(key) for key in params}
		# 请求资源映射字典中提取匹配的 处理器，如果找不到则调用notfound_404 处理
		handler = self.pathmap.get((method,path), self.notfound_404)
		# 分发请求处理
		return handler(environ,start_response)
	
	def notfound_404(self,environ,start_response):
		start_response('404 not found',[('Content-type','text/plain')])
		return [b'Not found']
	
	def register(self,method,path,function):
		self.pathmap[method.lower(),path] = function
		return function


class Rest_Handler:
	def hello_world(self,environ,start_response):
		# 响应头
		start_response('200 OK', [('Content-type','text/html')])
		# 从请求提中提取参数
		params = environ['params']
		
		# 响应页面渲染
		resp = _hello_resp = '''\
			<html>
				<head>
					<title>Hello {name}</title>
				</head>
				<body>
					<h1>Hello {name}!</h1>
				</body>
			</html>
		'''.format(name=params.get('name')).strip()
		
		# 返回页面
		yield resp.encode('utf-8')
	
	
	def localtime(self,environ,start_response):
		# 准备响应头
		start_response('200 OK',[('Content-type','application/xml')])
		t = time.localtime()
		# 响应页面渲染
		resp = '''\
			<?xml version='1.0'?>
			<time>
				<year>{t.tm_year}</year>
				<month>{t.tm_mon}</month>
				<day>{t.tm_mday}</day>
				<hour>{t.tm_hour}</hour>
				<minute>{t.tm_min}</minute>
				<second>{t.tm_sec}</second>
			</time>
		'''.format(t = t).strip()
		
		# 输出响应
		yield resp.encode('utf-8')


if __name__=="__main__":
	try:
		# 调度器
		dispatcher = PathDispatcher()
		# 控制器
		rest_handler = Rest_Handler()
		
		# 往调度器注册
		dispatcher.register('GET','/hello',rest_handler.hello_world)
		dispatcher.register('GET','/localtime',rest_handler.localtime)
		
		httpd = make_server('',8080,dispatcher)
		print('Serving on port 8080 ...')
		httpd.serve_forever()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)





