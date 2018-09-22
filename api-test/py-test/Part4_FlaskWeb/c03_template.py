#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/19'
Info:
	1）同级目录下创建templates目录，编辑html模板，变量使用{{var}}替代
	2）导入依赖模块from flask import render_template
	3）返回渲染页面return render_template('user.html',name=name)
	
	页面过滤器 <h1>Hello,{{name|capitalize}}!</h1>
	safe    渲染值时不转义
	capitalize  把值的首字母转换成大写，其他字母转换成小写
	lower   把值转换成小写形式
	upper   把值转换成大写形式
	title   把值中每个单词的首字母都转换成大写
	trim    把值的首尾空格去掉
	striptags   渲染之前把值中所有的 HTML 标签都删掉
	千万别在不可信的值上使用 safe 过滤器，例如用户在表单中输入的文本。
	完整过滤器列表 http://jinja.pocoo.org/docs/templates/#builtin-filters
	
	extends
	     <html>
	     <head>
			{% block head %}
			<title>{% block title %}{% endblock %} - My Application</title>
			{% endblock %}
		</head>
		<body>
			{% block body %}
			{% endblock %}
		</body>
		</html>
		
		block 标签定义的元素可在衍生模板中修改。在本例中，我们定义了名为 head、title 和
		body 的块。注意，title 包含在 head 中。下面这个示例是基模板的衍生模板:
		
		{% extends "base.html" %}
		{% block title %}Index{% endblock %} {% block head %}
		         {{ super() }}
		         <style>
		         </style>
		{% endblock %}
		{% block body %}
			<h1>Hello, World!</h1>
		{% endblock %}
		
		extends 指令声明这个模板衍生自 base.html。在 extends 指令之后，基模板中的 3 个块被 重新定义，
		模板引擎会将其插入适当的位置。注意新定义的 head 块，在基模板中其内容不 是空的，所以使用 super() 获取原来的内容。


"""

from flask import Flask,request,make_response,redirect,abort,render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap

from myobjs import *

app = Flask(__name__)
# manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	user_agent=request.headers.get('User-Agent')
	return render_template('index.html')


@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

@app.route('/test_attr')
def test_attr():
	mydict = dict()
	mydict['name'] = 'tom' # {{ mydict['key'] }}
	mylist=['apple','orange','banana','pinapple'] # mylist[3], mylist[myintvar]
	car = Car('Red',120,1000) # myobj.somemethod() 注：somemethod 只能在页面写死,不接受动态参数
	return render_template('test_attr.html',mydict=mydict,mylist=mylist,myintvar=2,myobj=car)

@app.route('/test_filter/<name>')
def test_filter(name):
	html = "<span style='color:red'>test safe</span>"
	return render_template('test_filter.html',name=name,html=html)


@app.route('/test_ctl')
def test_ctl():
	html = "<span style='color:red'>test safe</span>"
	return render_template('test_ctl.html',user='tom',comments=['apple','orange','banana','pinapple'])


@app.route('/test_extends')
def test_extends():
	return render_template('test_extends.html')

@app.route('/test_bootstrap')
def test_bootstrap():
	
	return




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
	app.run(debug=True)
	# manager.run()
	
