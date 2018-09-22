#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/19'
Info:
	0) pipenv2 install flask-bootstrap
	1) from flask_bootstrap import Bootstrap
	2) bootstrap = Bootstrap(app)
	3）基于Bootstrap组件自定义js块，需要 先调用{{ super() }}, 然后添加<script>
		例：
			{% block script %}
				{{ super() }}
				<script type='text/javascript' src='my-script.js'></script>
			{% endblock %}
	
	Flask-Bootstrap 基于模板定义的块
	doc             整个 HTML 文档
	html_attribs    <html> 标签的属性
	html            <html> 标签中的内容
	head            <head> 标签中的内容
	title           <title> 标签中的内容
	metas           一组 <meta> 标签
	styles          层叠样式表定义
	body_attribs    <body> 标签的属性
	body            <body> 标签中的内容
	navbar          用户定义的导航条
	content         用户定义的页面内容
	scripts         文档底部的 JavaScript 声明
	
	4) 异常页面 404 500  http://127.0.0.1:5000/abc
	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('404.html'),404
	
	注：404 可以手动触发，500 只有真实内部出现异常才会触发
	@app.errorhandler(500)
	def internal_error(e):
		return render_template('500.html'),500
	
	5) 翻译需要跳转的链接
	from flask import url_for
	
	print(url_for('index')) # 转换为相对路径'/'
	print(url_for('index',_external=True)) # 转换绝对路径 https://127.0.0.1:5000/,  _external=True 说明是给流量器之外使用，会自动转换为绝对地址
	print(url_for('test_bootstrap',name=name,_external=True)) # http://127.0.0.1:5000/test_bootstrap/Tom
	print(url_for('test_bootstrap',name=name,page=2,_external=True)) # http://127.0.0.1:5000/test_bootstrap/Tom?page=2 指定参数之外的 入参，以？方式呈现
	
	6) 静态文件 url_for('static', filename = 'favicon.ico')
	图标的声明会插入 head 块的末尾。注意如何使用 super() 保留基模板中定义的块的原始 内容。
	{% block head %}
	{{ super() }}
	<link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
	type="image/x-icon">
	<link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
	type="image/x-icon"> {% endblock %}
	
	7) 本地化日期时间
	pipenv2 install flask-monent
	from flask_moment import Moment
	monent = Moment(app)
	
	<!-- 时间转换 -->
	{% block scripts %}
	    {{ super() }}
	    {{ moment.include_moment() }}
	    {{ moment.lang('es') }} <!-- 语言 -->
	{% endblock %}
	
	<p>The local date and time is {{ moment(current_time).format('LLL') }}.</p>
    <p>That was {{ moment(current_time).fromNow(refresh=True) }}</p>
    
    注：format('LLL') 根据客户端电脑中的时区和区域设置渲染日期和时间。参数决定了渲染的方 式，'L' 到 'LLLL' 分别对应不同的复杂度。format() 函数还可接受自定义的格式说明符。
	
	第二行中的 fromNow() 渲染相对时间戳，而且会随着时间的推移自动刷新显示的时间。这 个时间戳最开始显示为“a few seconds ago”，但指定 refresh 参数后，其内容会随着时 间的推移而更新。
	如果一直待在这个页面，几分钟后，会看到显示的文本变成“a minute ago”“2 minutes ago”等。
	
	Flask-Moment 实现了 moment.js 中的 format()、fromNow()、fromTime()、calendar()、valueOf() 和 unix() 方法。
	
"""

from flask import Flask,request,make_response,redirect,abort,render_template,url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from myobjs import *

app = Flask(__name__)
# manager = Manager(app)
monent = Moment(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	user_agent=request.headers.get('User-Agent')
	return render_template('index.html',current_time=datetime.utcnow())

@app.route('/test_bootstrap/<name>')
def test_bootstrap(name):
	return render_template('test_bootstrap.html',name=name)

@app.route('/test_url_for/<name>')
def test_url_for(name):
	name = str(name).capitalize()
	print(url_for('index')) # 转换为相对路径'/'
	print(url_for('index',_external=True)) # 转换绝对路径 https://127.0.0.1:5000/,  _external=True 说明是给流量器之外使用，会自动转换为绝对地址
	print(url_for('test_bootstrap',name=name,_external=True)) # http://127.0.0.1:5000/test_bootstrap/Tom
	print(url_for('test_bootstrap',name=name,page=2,_external=True)) # http://127.0.0.1:5000/test_bootstrap/Tom?page=2 指定参数之外的 入参，以？方式呈现
	
	return render_template('test_bootstrap.html',name=name)
	
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500



# debug 模式启动服务，自动刷新
if __name__=='__main__':
	app.run(debug=True)
	# manager.run()
	
