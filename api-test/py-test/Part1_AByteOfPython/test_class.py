#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/16'
Info:
        
"""
import os,traceback

class Person:
	age = 18  # 类属性
	def __init__(self,name):  # 定义构造器同时，绑定了属性，对象属性
		self.name = name
	
	def sayHi(self):
		print("hello,everybody {name} ,{age}".format(name=self.name,age=self.age))  # 取变量

class Robot:
	'''Represents a robot, with a name'''
	population = 0 # 公共属性不需要 __ 前缀
	
	def __init__(self,name):
		'''Inititlize the data'''
		self.__name = name  # 私有属性 使用 "__field" 前缀标识
		print("Initialize {0}".format(self.__name))
		
		# add when initlization
		Robot.population += 1

	def __del__(self):
		'''dying'''
		print("{0} is being destoryed!".format(self.__name))
		
		Robot.population -=1
		
		if Robot.population ==0:
			print("{0} was the last one".format(self.__name))
		else:
			print("There are still {0:d} robots working.".format(Robot.population))


	def sayHi(self):  # 方法 带 __ 前缀，只能在 class 内部被调用
		'''Greeting by the robot
		Yeah, they can do that.
		'''
		print("Greetings, my master call me {0}".format(self.name))

	@staticmethod # 等价于 howMany = staticmethod(howMany)
	def howMany(): # 静态函数不需要 self 入参
		'''print the current population'''
		print("We have {0:d} robots".format(Robot.population)) # {0:d} 序号为0,整形

class SchoolMember:
	'''Represent any school member.'''
	def __init__(self,name,age):
		self.name = name
		self.age =age
		print("Initialize SchoolMember: {0}".format(self.name))
	
	def tell(self):
		'''Tell my details'''
		print("Name:{0}, Age:{1}".format(self.name,self.age),end='')

class Teacher(SchoolMember): # 子类集成父类
	'''Repressent a teacher'''
	def __init__(self,name,age,salary):
		SchoolMember.__init__(self,name,age)  # 子类实例创建，现式调用了父类构造器，并且传入了子类对象自身
		self.salary = salary
		print("Salary: {0:d}".format(self.salary))

	def tell(self):
		SchoolMember.tell(self)
		print("Salary: {0:d}".format(self.salary))
		
class Student(SchoolMember):
	'''Represents a student'''
	def __init__(self,name,age,marks):
		SchoolMember.__init__(self,name,age)
		self.marks = marks
		print("Initialize Student: {0}".format(self.name))
	
	def tell(self):
		SchoolMember.tell(self)
		print("Marks: {0:d}".format(self.marks))


def __test_init():
	p1 = Person("Tom") # 调用有参构造器创建对象
	p1.sayHi()
	
	p2 = Person("Jack")
	p2.age=20  # 修改了对象属性
	p2.sayHi()
	p1.sayHi()
	
	Person.age=20 # 修改了类属性
	p2.sayHi()
	p1.sayHi()

def test_fields():
	droid1 = Robot('R2-D2')
	droid1.sayHi()
	droid2 = Robot('C-3')
	droid2.sayHi()
	
	del droid1  # __buildin__ 中的 del 操作，会调用到 class 中的 __del__(self) 函数
	
	Robot.howMany()
	
	del droid2
	Robot.howMany()
	
	print(Robot.__doc__)
	




if __name__=="__main__":
	try:
		# test_init()
		# test_fields()
		
		t = Teacher("Tom",30,200000)
		s = Teacher("Jack",25,75)
		
		members = [t,s]
		
		for m in members:
			m.tell()
		
	except:
		traceback.print_exc()
	finally:
		os._exit(0)

