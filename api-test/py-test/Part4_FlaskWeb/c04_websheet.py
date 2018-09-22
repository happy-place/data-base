#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/19'
Info:
	默认情况下，Flask-WTF 能保护所有表单免受跨站请求伪造(Cross-Site Request Forgery，CSRF)的攻击。恶意网站把请求发送到被攻击者已登录的其他网站时就会引发 CSRF 攻击。

	1) pipenv install flask-wtf
	2）app.config 字典可用来存储框架、扩展和程序本身的配置变量。使用标准的字典句法就能 把配置值添加到 app.config 对象中。
	   这个对象还提供了一些方法，可以从文件或环境中导 入配置值。
		app = Flask(__name__)
		app.config['SECRET_KEY']='hard to guess string'
		
	3) 继承 flask_wtf 的 Form 类，创建自定义的实例
	from flask_wtf import Form
	from wtforms import StringField,SubmitField
	from wtforms.validators import Required
	
	class NameForm(Form):
		name = StringField("What is your name?",validators=[Required()])
		submit = SubmitField('Submit')
		
	4）编写请求表单页直接对表单页 test_form.html 返回 form 实例
	@app.route('/test_form/')
	def test_form():
		nameform = NameForm()
		return render_template('test_form.html',form = nameform)
	
	5）编辑表单html 模板
	{% extends "bootstrap-base.html" %} <!-- 继承现有flask-bootstrap 插件-->

	{% block content %}  <!-- 覆盖内容页 -->
	<div class="container">
	    <div class="page-header">
	        <form method="POST">  <!-- 表单页 -->
	            {{form.hidden_tag()}}
	            {{form.name.label}} {{form.name(id='my-text-field')}} <!-- 设置 id 指定css 样式 -->
	            {{form.submit}}
	        </form>
	    </div>
	</div>
	{% endblock %}
	
	6）加速页面渲染
	Flask-Bootstrap 提供了一个非常高端的辅助函 数，可以使用 Bootstrap 中预先定义好的表单样式渲染整个 Flask-WTF 表单，
	而这些操作 只需一次调用即可完成。
	{% extends "bootstrap-base.html" %} <!-- 继承现有flask-bootstrap 插件-->
	{% import "bootstrap/wtf.html" as wtf %}
	
	{% block content %}  <!-- 覆盖内容页 -->
	<div class="container">
	    <div class="page-header">
	        <h1>Hello, {% if name %} {{name}} {% else %}Stranger{% endif %}</h1>
	        {{ wtf.quick_form(form)}}
	    </div>
	</div>
	{% endblock %}
	
	7) 同时处理 GET 和 POST 请求
	@app.route('/test_form/',methods=['GET','POST'])
	
	8）防止空串提交
	客户端验证：
		class NameForm(Form):
			# 如果用户提交表单之前没有输入名字，Required() 验证函数会捕获这个错误
			name = StringField("What is your name?",validators=[Required()])  <<< validators=[Required() 直接在客户端进行验证
			submit = SubmitField('Submit')
	服务端验证
		if form.validate_on_submit():
	
	9）防止表单重复提交
		原理：表单提交成功后，使用重定向机制 redirect 替代默认的 render_template (forward) 机制 跳转到成功页面
		from flask import redirect
		return redirect(url_for('test_bootstrap',name=session['name'],_external=True))
		
	10）多次请求间保存状态
		from flask import session
		
		if form.validate_on_submit():
			....
			session['name'] = form.name.data   # 某次成功请求，完成验证，需要保存状态
		else:
			# 下次再次来到相应页面，可以取会上次提交的信息
			return render_template('test_form.html',form = form,name=session.get('name'))
			
		<h1>Hello, {% if name %} {{name}} {% else %}Stranger{% endif %}</h1> 页面回显
	
	11) Flash 消息
	发送消息
	from flask import flash
	flash('Looks like you have changed your name!')
	
	html页面显示消息
	{% for message in get_flashed_messages() %}
        <div class="alert alert-warning">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            {{ message }}
        </div>
    {% endfor %}
	
	
	
"""

from flask import Flask,request,make_response,redirect,abort,render_template,url_for,session,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

from myobjs import *

app = Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'
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

@app.route('/test_form/',methods=['GET','POST']) # 同时处理表单页请求 和 表单提交请求
def get_form():
	form = NameForm()
	if form.validate_on_submit(): # 正常提交
		new_name= form.name.data
		old_name = session['name']
		
		# 两次提交名称不一致，发消息提示
		if old_name is not None and old_name != new_name:
			flash('Looks like you have changed your name!')
		session['name'] = new_name
		
		print('提价验证通过')
		# return render_template('test_bootstrap.html',name=name) # 默认是 forward 机制，存在表单重复提交问题
		print(url_for('test_bootstrap',name=session['name'],_external=True)) # http://127.0.0.1:5000/test_bootstrap/tom
		return redirect(url_for('test_bootstrap',name=session['name'],_external=True)) # 使用重定向，放在表单重复提交
	else: # 空白提交
		print('提交为空')
		# 已经提交过表单的页面，再次获取表单页时，可以从session 中恢复 name, 当session 在通过 get 获取失败时，返回None
		return render_template('test_form.html',form = form,name=session.get('name'))

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
	
