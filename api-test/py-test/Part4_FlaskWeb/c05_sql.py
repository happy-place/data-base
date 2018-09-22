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
		
	2) 带参启动，shell中调试
		manager = Manager(app)
		if __name__=='__main__':
			# app.run(debug=True)
			manager.run()
			
		pyenv2 c05_sql.py shell
		>>> from c05_sql_test import *
		>>> db
		<SQLAlchemy engine=sqlite:////Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/data.sqlite>
		>>> db.create_all()  # 提交时，在basedir 指定目录下创建了data.sqlite文件（数据库存车数据文件）
		>>> db.drop_all() # 清库
		>>> db.create_all() # 重新建库
		>>> admin_role = Role(name='Admin')
		>>> mod_role = Role(name='Moderator')
		>>> user_role = Role(name='User')
		>>> user_john = User(username='john',role=admin_role)
        >>> user_susan = User(username='susan',role=user_role)
        >>> user_david = User(username='david',role=user_role)
        >>> print(admin_role.id) # 目前创建的对象暂时是游离态，尚未持久化
			None
		>>> db.session.add(admin_role) # 分步提交
		>>> db.session.add(mod_role)
		>>> db.session.add(user_role)
		>>> db.session.add(user_john)
		>>> db.session.add(user_susan)
		>>> db.session.add(user_david)
		
		>>> db.session.add_all([admin_role,mod_role,user_role,user_john,user_susan,user_david]) # 一次性提交
		
		>>> print(admin_role.id) # 事务未提交，仍然是游离态，此时如果只选 db.session.rollback() 则之前的add 全部回滚
			None
			
		>>> db.session.commit() # 提交事务
		
		>>> print(admin_role.id) # 成功落盘
		
		>>> user_david1 = User(username='david1',role=user_role)  # 创建User实例
		>>> db.session.add(user_david1) # 添加到session
		>>> print(user_david1.id)
		None
		>>> db.session.rollback() # 回滚，撤销添加
		>>> db.session.commit() # 提交
		>>> print(user_david1.id)   # 验证回滚逻辑
		None

		>>> print(mod_role.id)   # 删除操作演示，直接操作 pojo
			2
		>>> db.session.delete(mod_role) # 执行数据库删除
		>>> print(mod_role.id)  # 删除未提交，pojo 依旧存在
			2
		>>> db.session.commit() # 提交session
		>>> print(mod_role.id)  # mod_role 对象从持久态转换为游离态，操作游离态对象，其id 依旧存在
			2
		>>> Role.query.filter_by(name='Moderator').first() # 查库，发现数据库内依旧没有了
		>>> Role.query.filter_by(name='Admin').first()
			<Role u'Admin'>
		>>> Role.query.filter_by(id=2).first()
		>>> Role.query.filter_by(id=1).first()
			<Role u'Admin'>
			
		>>> print(str(Role.query.filter_by(name='Moderator'))) # 获取底层查询语句，执行 first() 算子时直接取值，就不会打印sql
			SELECT roles.id AS roles_id, roles.name AS roles_name
			FROM roles
			WHERE roles.name = ?
		
		>>> user_role_members=user_role.users # lazy='dynamic' 延迟加载查询
		>>> user_role_members
			<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x103c16190>
		>>> print(str(user_role_members)) # 生成了查询对象
			SELECT users.id AS users_id, users.username AS users_username, users.role_id AS users_role_id
			FROM users
			WHERE ? = users.role_id

		>>> user_role_members[0].role # 取第一个
			<Role u'User'>
		>>> user_role_members.order_by(User.username).all() # 直接基于Pojo 进行查询
		>>> [<User u'david'>, <User u'susan'>]
		>>> print(str(user_role_members.order_by(User.username)))
			SELECT users.id AS users_id, users.username AS users_username, users.role_id AS users_role_id
			FROM users
			WHERE ? = users.role_id ORDER BY users.username
			
		>>> user_role_members.count() # 统计格式
			2
			
		>>> print(str(User.query))
			SELECT users.id AS users_id, users.username AS users_username, users.role_id AS users_role_id
			FROM users
			
		>>> User.query.all() # 对 User类调用query api的all()函数
			[<User u'john'>, <User u'susan'>, <User u'david'>]
			
		>>> user_john = User.query.filter_by(username='john').first() # 提取
		>>> user_john.id
			1
		>>> user_john.role = user_role # 修改
		>>> db.session.commit() # 提交

		>>> user_role_members.count() # 验证
			3
		
	3）简单登录表单验证
		@app.route('/',methods=['GET','POST'])  # 同时处理 GET 和 POST
		def index():
			form = NameForm()
			if form.validate_on_submit():
				login_username = form.name.data # 表单传入登录名
				user = User.query.filter_by(username=login_username).first() # 查表取出对象，如果未找到返回 None
				if user is None:
					user = User(username=login_username)
					db.session.add(user) # 添加新user 到db
					session['known'] = False # 标记是新用户
				else:
					session['known'] = True  # 标记为老用户
				session['name'] = login_username # 缓存到 web-session
				form.name.data = '' # 表单置空
				return redirect(url_for('index')) # 重定向到成功页面，防止重复提交
			# 验证失败，重新退回 session.get('known',False) 存在known 就取出，否则使用默认值False
			return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))
		
		表单页
			{% extends "bootstrap-base.html" %} <!-- 继承现有flask-bootstrap 插件-->
			{% import "bootstrap/wtf.html" as wtf %} <!-- 映入表单模板 -->
			
			{% block content %}  <!-- 覆盖内容页 -->
			<div class="container">
			    <div class="page-header">
			        <h1> Hello, {% if name %} {{name}} {% else %}Stranger{% endif %} </h1> <!-- 从 response 提取name-->
			        {{ wtf.quick_form(form)}} <!-- 只需首次加载，其后直接使用 -->
			        {% if not known %} <!-- 从 resp 中取值，检测提交验证是否通过 -->
			        <p>Pleased to meet you!</p>
			        {% else %}
			        <p>Happy to see you again!</p>
			        {% endif %}
			    </div>
			</div>
			{% endblock %}

	4) 为 shell命令添加上下文
		from flask_script import Manager,Shell  # Manager 保证带参启动，Shell可以通过回调函数预先加载一些内容
		def make_shell_context():
			return dict(app=app,db=db,User=User,Role=Role)
		
		manager = Manager(app)
		manager.add_command('shell',Shell(make_context=make_shell_context)) # 设置shell 启动回调函数
		
		pyenv2 c05_sql.py shell  # 此时，直接进入 python 环境，并默认已经执行了 make_shell_context() 函数，即导入了 db,User,Role
		>>> User
			<class '__main__.User'>
		>>> User.query.all()
			[<User u'john'>, <User u'susan'>, <User u'david'>, <User u'tom'>]

	5) 数据库迁移
		pipenv2 install flask-migrate
		
		from flask_migrate import Migrate,MigrateCommand
		
		db = SQLAlchemy(app)
		manager = Manager(app)
		
		migrate = Migrate(app,db)
		manager.add_command('db',MigrateCommand) # 通过 db 命令 在manager 上附加 迁移类MigrateCommand
		
		pyenv2 c05_sql.py db init # 初始化迁移仓库，在当前脚本所在目录下创建了migrations 目录，生成相应迁移版本维护文件
			注：数据库迁移仓库中的文件要和程序的其他文件一起纳入版本控制。
		    Creating directory /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/migrations ... done
			Creating directory /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/migrations/versions ... done
			Generating /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/migrations/alembic.ini ... done
			Generating /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/migrations/env.py ... done
			Generating /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/migrations/env.pyc ... done
			Generating /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/migrations/README ... done
			Generating /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/migrations/script.py.mako ... done
			Please edit configuration/connection/logging settings in '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/migrations/alembic.ini' before
			proceeding.
		
		pyenv2 c05_sql.py db migrate -m "initial migration" # 创建了迁移脚本 b55cdc3cb63a_upgrade.py，此时upgrade 和 downgrade 都是空的
			INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
			INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
			INFO  [alembic.env] No changes in schema detected.
			在 Alembic 中，数据库迁移用迁移脚本表示。脚本中有两个函数，分别是 upgrade() 和 downgrade()。upgrade()
			函数把迁移中的改动应用到数据库中，downgrade() 函数则将改动 删除。Alembic 具有添加和删除改动的能力，
			因此数据库可重设到修改历史的任意一点。
		
		。。。。。 修改 db 相关的 User Role 类
		
		pyenv2 c05_sql.py db upgrade  # 将改动同步到数据库的模型中，迁移脚本被填充了如下内容
		# b55cdc3cb63a_upgrade.py
		------------------------------------------------------------------------
		def upgrade():
		    # ### commands auto generated by Alembic - please adjust! ###
		    op.create_table('students',
		    sa.Column('id', sa.Integer(), nullable=False),
		    sa.Column('username', sa.String(length=64), nullable=True),
		    sa.Column('role_id', sa.Integer(), nullable=True),
		    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
		    sa.PrimaryKeyConstraint('id')
		    )
		    op.create_index(op.f('ix_students_username'), 'students', ['username'], unique=True)
		    # ### end Alembic commands ###
		------------------------------------------------------------------------
		
		。。。。 再次修改 db 相关的 User Role 类
		
		pyenv2 c05_sql.py db downgrade
		# b55cdc3cb63a_upgrade.py
		------------------------------------------------------------------------
		def downgrade():
		    # ### commands auto generated by Alembic - please adjust! ###
		    op.drop_index(op.f('ix_students_username'), table_name='students')
		    op.drop_table('students')
		    # ### end Alembic commands ###
		------------------------------------------------------------------------

		
		我们可以使用 revision 命令手动创建 Alembic 迁移，也可使用 migrate 命令自动创建。 手动创建的迁移只是一个骨架，upgrade()
		和 downgrade() 函数都是空的，开发者要使用.Alembic 提供的 Operations 对象指令实现具体操作。自动创建的迁移会根据模型定义和数
		据库当前状态之间的差异生成 upgrade() 和 downgrade() 函数的内容。

		自动创建的迁移不一定总是正确的，有可能会漏掉一些细节。自动生成迁移 脚本后一定要进行检查。
		
		如果你从 GitHub 上克隆了这个程序的 Git 仓库，请删除数据库文件 data. sqlite，然后执行 Flask-Migrate 提供的 upgrade 命令，
		使用这个迁移框架重新 生成数据库。
	
"""
import os
from flask import Flask,request,make_response,redirect,abort,render_template,url_for,session,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand

from myobjs import *

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
manager = Manager(app)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role)

manager.add_command('shell',Shell(make_context=make_shell_context))

monent = Moment(app)
bootstrap = Bootstrap(app)

class Role(db.Model):
	__tablename__='roles'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	users = db.relationship('User',backref='role',lazy='dynamic') #
	
	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),unique=True,index=True)
	role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
	
	def __repr__(self):
		return '<User %r>' % self.username

# class Students(db.Model):
# 	__tablename__='students'
# 	id = db.Column(db.Integer,primary_key=True)
# 	username = db.Column(db.String(64),unique=True,index=True)
# 	role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
#
# 	def __repr__(self):
# 		return '<User %r>' % self.username


@app.route('/',methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))

# @app.errorhandler(500)
# def internal_server_error(e):
# 	return render_template('500.html'), 500

# debug 模式启动服务，自动刷新
if __name__=='__main__':
	# app.run(debug=True)
	manager.run()
	
