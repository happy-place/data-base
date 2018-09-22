#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/20'
Info:
        
"""
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class Car:
	def __init__(self,color,speed,price):
		self.color = color
		self.speed = speed
		self.price = price
		self.price = price
	
	def info(self):
		items = 'color:{color}, speed:{speed}, price:{price}'.format(color=self.color,speed=self.speed,price=self.price)
		return '{myclass}: {items}'.format(myclass=self.__class__.__name__,items=items)

# 通过继承关系，可以直接将一个自定义的NameForm实例传递给 html 页面进行展示
class NameForm(FlaskForm):
	# 如果用户提交表单之前没有输入名字，Required() 验证函数会捕获这个错误
	name = StringField("What is your name?",validators=[Required()])
	submit = SubmitField('Submit')
	


