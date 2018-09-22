#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/19'
Info:

	MySQL               mysql://username:password@hostname/database
	Postgres            postgresql://username:password@hostname/database
	SQLite(Unix)        sqlite:////absolute/path/to/database
	SQLite(Windows)     sqlite:///c:/absolute/path/to/database
	
	一对多关系：
	方案1: 正向关联
	    class User(db.Model):
	         # ...
	         role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
        
    方案2：反向引用（等效于上面的 db.ForeignKey ）
        class Role(db.Model):
	         # ...
	         users = db.relationship('User', backref='role')
	
	数据库选型：
		传统 RDBMS 关系型数据库遵循：字段定义唯一，表必须包含主键，表与表只能通过主外键发送关联的原则，最大程度减少了冗余字段问题；
		非关系型数据库 NoSQL,实质是指KV结构存储的数据库，通常不利于连表操作，存在维度冗余问题，但能提高查询效率；
	Flask 基于Flask_SQLAlchemy 框架，类似于传统hibernate 插件，实现了业务层与数据库的解耦，基于完善的ORM映射关系操作数据库。以牺牲性能为代价
	提高了数据库操作的查询效率。
	
	1）建模
	    pipenv2 install flask-sqlalchemy
	    数据库引擎           URL
	    MySQL               mysql://username:password@hostname/database
		Postgres            postgresql://username:password@hostname/database
		SQLite(Unix)        sqlite:////absolute/path/to/database
		SQLite(Windows)     sqlite:///c:/absolute/path/to/database
     
        依赖问题
	    from flask_sqlalchemy import SQLAlchemy
	 
		basedir = os.path.abspath(os.path.dirname(__file__))
		app = Flask(__name__)
		app.config['SECRET_KEY']='hard to guess string'
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	
	    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 将会追踪对象的修改并且发送信号，需要消耗额外内存
		app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 关机时自动提交
		
		db = SQLAlchemy(app)
		
		模型：
		class Role(db.Model):
			__tablename__='roles'  # 表名
			id = db.Column(db.Integer,primary_key=True) # 主键 int类型，创建索引
			name = db.Column(db.String(64),unique=True) # 唯一约束
			
			# 反向绑定 User 表，建立一对多关联关系，此处User 类肯能还未创建，所以使用字面量，
			# lazy='dynamic'延迟加载，role.users 返回的是 类sql 的查询语句
			users = db.relationship('User',backref='role',lazy='dynamic')
			
			# 格式化输出
			def __repr__(self):
				return '<Role %r>' % self.name
		
		class User(db.Model):
			__tablename__='users' # 表名
			id = db.Column(db.Integer,primary_key=True) # 主键 int 类型
			username = db.Column(db.String(64),unique=True,index=True) # 唯一约束，创建索引
			role_id = db.Column(db.Integer,db.ForeignKey('roles.id')) # 外键管理Role的主键
			
			# 格式化输出
			def __repr__(self):
				return '<User %r>' % self.username

	
 
"""
import os
from flask import Flask,request,make_response,redirect,abort,render_template,url_for,session,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy

from myobjs import *

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

# def make_shell_context():
# 	return dict(app=app,db=db,User=User,Role=Role)

manager = Manager(app)
# manager.add_command('shell',Shell(make_context=make_shell_context))

# monent = Moment(app)
# bootstrap = Bootstrap(app)

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


# @app.route('/',methods=['GET','POST'])
# def index():
# 	form = NameForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(username=form.name.data).first()
# 		if user is None:
# 			user = User(username=form.name.data)
# 			db.session.add(user)
# 			session['known'] = False
# 		else:
# 			session['known'] = True
# 		session['name'] = form.name.data
# 		form.name.data = ''
# 		return redirect(url_for('index'))
# 	return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))
#
# # @app.errorhandler(500)
# # def internal_server_error(e):
# # 	return render_template('500.html'), 500


# debug 模式启动服务，自动刷新
if __name__=='__main__':
	# app.run(debug=True)
	manager.run()
	
