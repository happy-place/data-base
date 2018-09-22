#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/19'
Info:
	0).app.run(debug=True)启动模式不能接受启动参数调用，借助 Flask-Script 可实现带参数启动效果；
	1).pipenv2 install flask-script  安装 flask-script 模块到 venv 环境
	2).修改代码
		app = Flask(__name__)
		manager = Manager(app)
		
		if __name__=='__main__':
			# app.run(debug=True)
			manager.run()
			
		注：一旦使用manager.run()启动，不能使用 debug=True 参数，
		
		huhao:Part4_Flaskweb huhao$ pyenv2 c03_manager.py --help   << 查看帮助信息
		usage: c03_manager.py [-?] {shell,runserver} ... <<< 可选入参  [-?], 必选参数 {shell,runserver}
		
		positional arguments:
		  {shell,runserver}
		    shell            Runs a Python shell inside Flask application context.   Flask 应用上下文中运行 Python shell
		    runserver        Runs the Flask development server i.e. app.run() 运行 Flask 开发服务器:app.run()
		
		optional arguments:
		  -?, --help         show this help message and exit
		  
		 pyenv2 c03_manager.py --host 0.0.0.0  <<< 通过 127.0.0.1 或 外网ip 都能正常访问
		 这是右键启动参数 Run > Edit Configurations > Parameters: runserver --host 127.0.0.1

	




"""

from flask import Flask,request,make_response,redirect,abort
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
	user_agent=request.headers.get('User-Agent')
	return '<h1>Your browser is %s!</h1>' % user_agent
	

@app.route('/user/<name>')
def user(name):
	return '<h1>Hello,%s!</h1>' % name


@app.route('/user/<int:age>')
def age(age):
	return '<h1>Hello,%d!</h1>' % age

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
	# app.run(debug=True)
	manager.run()
