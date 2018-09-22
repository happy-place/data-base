#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/19'
Info:
	1) 安装
	    pipenv2 install flask-mail
		from flask_mail import Mail,Message
	2）配置
		import os
		from flask import Flask
		from flask_script import Manager,Shell
		from flask_mail import Mail,Message

		app = Flask(__name__)

		app.config['MAIL_SERVER'] = 'smtp.qq.com'
		app.config['MAIL_PORT'] = 587
		app.config['MAIL_USE_TLS'] = True

		# 方案1： 直接将邮箱名 和 密钥写死（不推荐）
		# app.config['MAIL_USERNAME'] = '101798447871@qq.com'
		# app.config['MAIL_PASSWORD'] = 'untblapsprgebccbsj'
		# 方案2：在shell 环境中export MAIL_USERNAME 和 MAIL_PASSWORD，然后自动从环境中获取（推荐）
		# 模拟通过环境提取用户名 和 密钥 等敏感信息
		app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
		app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

	3） 创建邮件对象 和 发送函数
		mail = Mail(app)
		manager = Manager(app)

		def send_test():
			msg = Message('test subject',sender='1017984471@qq.com',recipients=['huhao1@cmcm.com',])
			msg.body = 'text body'
			msg.html = '<b>HTML</b> body'
			with app.app_context():
				mail.send(msg)

	4）环境设置
		source flasky/venv/bin/activate

		(venv) huhao:Part4_FlaskWeb huhao$ export MAIL_USERNAME='101798884471@qq.com'
		(venv) huhao:Part4_FlaskWeb huhao$ export MAIL_PASSWORD='untblapsprgebccbsj'

		(venv) huhao:Part4_FlaskWeb huhao$ pyenv2 06_email.py shell
		>>> from c06_email import *
		>>> send_test()

	5）编码发送邮件，实现新登录用户自动向管理员发送邮件 的功能 (同步发送)
		app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
		app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <1017984471@qq.com>'
	
		def send_mail(to,subject,template,**kwargs):
			# 组织消息
			msg = Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
			              sender=app.config['FLASKY_MAIL_SENDER'],
			              recipients=[to])
			              
			# 配置 txt ,html 格式模板
			msg.body = render_template(template+'.txt',**kwargs)
			msg.html = render_template(template+'.html',**kwargs)
			
			# 发送
			mail.send(msg)
	
	6）表单提交流程
	@app.route('/',methods=['GET','POST'])
	def index():
		form = NameForm()
		if form.validate_on_submit(): # 拦截POST请求，并将请求体封装到 form 中
			user = User.query.filter_by(username=form.name.data).first() # 查库
			if user is None: # 库中不存在，说明是新人
				user = User(username=form.name.data) # 封装游离态 实例
				db.session.add(user) # 落盘 转为持久态
				session['known'] = False # 判断是否是新人标记
				
				if app.config['FLASKY_ADMIN']: # 如果配置了管理员，就想管理员发送邮件
					send_mail(to=app.config['FLASKY_ADMIN'],subject='New User',template='mail/new_user',user=user)
				
			else:
				session['known'] = True # 标记为是已经存在的对象
			session['name'] = form.name.data #  不管是否是新人，都将用户名提取到 web-session 中保存
			form.name.data = '' # 表单指控
			return redirect(url_for('index')) # 重定向到成功页
		# 如果不是POST 提交，就直接返回空表单对象
		return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))

	7）准备模板 templates/mail/new_user.html,new_user.txt
			new_user.html:
				User <b>{{ user.username }}</b> has joined.
			new_user.txt
				User {{ user.username }} has joined.
				
	8）异步发送
		from threading import Thread # 使用多线程
		
		def send_async_email(app,msg):
			with app.app_context():
				mail.send(msg)
		
		def send_mail(to,subject,template,**kwargs):
			msg = Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
			              sender=app.config['FLASKY_MAIL_SENDER'],
			              recipients=[to])
			
			msg.body = render_template(template+'.txt',**kwargs)
			msg.html = render_template(template+'.html',**kwargs)
			
			# 使用多线程发送，邮件，认证通过直接返回响应页面，邮件等待异步发送，体验更为流畅
			asyc_thread = Thread(target=send_async_email,args=[app,msg])
			asyc_thread.start()
			
			return asyc_thread
			
	不过要记住，程序要发送大量电子邮件时，使 用专门发送电子邮件的作业要比给每封邮件都新建一个线程更合适。例如，我们可以把执 行 send_async_email()
	函数的操作发给 Celery(http://www.celeryproject.org/)任务队列。
		
	
mypip2 install flask flask_bootstrap flask_moment flask_script flask_sqlalchemy flask_migrate flask_mail threading
"""
import os
from flask import Flask,request,make_response,redirect,abort,render_template,url_for,session,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message

from threading import Thread


from myobjs import *

app = Flask(__name__)
monent = Moment(app)
bootstrap = Bootstrap(app)

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '1017984471@qq.com'
app.config['MAIL_PASSWORD'] = 'untblapsprgebccb'
app.config['FLASKY_ADMIN'] = 'huhao1@cmcm.com'

# 模拟通过环境提取用户名 和 密钥 等敏感信息
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# app.config['FLASKY_ADMIN'] =  os.environ.get('FLASKY_ADMIN')

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <1017984471@qq.com>'


mail = Mail(app)
manager = Manager(app)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Role(db.Model):
	__tablename__='roles'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	users = db.relationship('User',backref='role',lazy='dynamic') # 反向添加应用，相当于到
	
	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),unique=True,index=True)
	role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
	
	def __repr__(self):
		return '<User %r>' % self.username


def send_test():
	msg = Message(subject='test subject',sender='1017984471@qq.com',recipients=['huhao1@cmcm.com',])
	msg.body = 'text body'
	msg.html = '<b>HTML</b> body'
	with app.app_context():
		mail.send(msg)

def send_mail_sync(to,subject,template,**kwargs):
	msg = Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
	              sender=app.config['FLASKY_MAIL_SENDER'],
	              recipients=[to])
	
	# msg.body = render_template(template+'.txt',**kwargs)
	msg.html = render_template(template+'.html',**kwargs)
	
	send_async_email(app,msg)
	
def send_async_email(app,msg):
	with app.app_context():
		mail.send(msg)

def send_mail(to,subject,template,**kwargs):
	msg = Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
	              sender=app.config['FLASKY_MAIL_SENDER'],
	              recipients=[to])
	
	msg.body = render_template(template+'.txt',**kwargs)
	msg.html = render_template(template+'.html',**kwargs)
	
	asyc_thread = Thread(target=send_async_email,args=[app,msg])
	asyc_thread.start()
	
	return asyc_thread


@app.route('/',methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known'] = False
			
			if app.config['FLASKY_ADMIN']:
				send_mail(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
			
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))



# debug 模式启动服务，自动刷新
if __name__=='__main__':
	# app.run(debug=True)
	manager.run()
	
