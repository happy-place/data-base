#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/19'
Info:
所有 Flask 程序都必须创建一个程序实例。Web 服务器使用一种名为 Web 服务器网关接口 (Web Server Gateway Interface，WSGI)的协议
"""

from flask import Flask,request,make_response,redirect,abort

# 创建服务端点实例
app = Flask(__name__)

# 被  @app.route 注解的函数称为视图函数
# http://127.0.0.1:5000/
@app.route('/')
def index():
	'''
	Flask 使用上下文让特定变量在线程全局可访问，同时与其他线程互不干扰
	线程是可单独管理的最小指令集。进程经常使用多个活动线程，有时还会共 享内存或文件句柄等资源。多线程 Web 服务器会创建一个线程池，
	再从线 程池中选择一个线程用于处理接收到的请求。

	上下文变量
	current_app 当前激活程序实例
	g 处理请求是用作临时存储的对象。每次请求都会重置此对象
    request 请求对象，封装客户端发出的http 请求内容
    session 用户回话，封装了各请求间需要记住测值得字典
    
    python shell 演示程序上下文回话
    
    python c02_helloworld.py # 启动app
    python  # 进入python 命令行
    >>> import flask                    # 导入fask 模块
    >>> fromc c02_helloworld import app  # 导入 app 实例
    >>> current_app.name                # 获取 app 名称失败
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ...
    RuntimeError: Working outside of application context.
	>>> app_ctx = app.app_context()   # 提取正在运行app名称 注意，在程序实例上调用 app.app_context() 可获得一个程序上 下文。
	>>> app_ctx.push()                # 将正在运行app实例的上下文推送给Flask的app应用程序
	>>> current_app.name()            # 再次获取正在运行app实例名称
	'c02_helloworld'
    >>> app_ctx.pop()                 # 取消到Flask的app应用程序的注册
      >>> current_app.name                # 获取 app 名称失败
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ...
    RuntimeError: Working outside of application context.
    
    >>> app.url_map  <<< 查看映射关系
	Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
	 <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
	 <Rule '/user/<age>' (HEAD, OPTIONS, GET) -> age>,
	 <Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>])

	请求钩子
	• before_first_request:注册一个函数，在处理第一个请求之前运行。
	• before_request:注册一个函数，在每次请求之前运行。
	• after_request:注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
	• teardown_request:注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。
	在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量 g。例如，before_ request 处理程序可以从数据库中加载已登录用户，
	并将其保存到 g.user 中。随后调用视 图函数时，视图函数再使用 g.user 获取用户。
	
	
	'''
	user_agent=request.headers.get('User-Agent')
	return '<h1>Your browser is %s!</h1>' % user_agent
	
# 请求调度通过 @app.route 注册 或 app.add_url_rule() 注册
# http://127.0.0.1:5000/user/tom
@app.route('/user/<name>')
def user(name):
	return '<h1>Hello,%s!</h1>' % name

# http://127.0.0.1:5000/user/20
@app.route('/user/<int:age>')
def age(age):
	return '<h1>Hello,%d!</h1>' % age

# 添加响应状态码 http://127.0.0.1:5000/redirect_page
@app.route('/test_status')
def test_status():
	return '<h1>test_status!</h1>',303

@app.route('/test_cookie')
def test_cookie():
	response = make_response('<h1>test cookie</h1>',303)
	# response.set_cookie('name','tom')
	return response

@app.route('/test_redirect')
def test_redirect():
	return redirect('http://www.python.org')

# 404 响应
@app.route('/test_abort/<id>')
def test_abort(id):
	res = {'1':'tom','2':'lucy'}
	if not res.keys().__contains__(id):
		abort(404)
	return '<h1>hello, %s!</h1>' % res[id],200


# debug 模式启动服务，自动刷新
if __name__=='__main__':
	app.run(debug=True)
