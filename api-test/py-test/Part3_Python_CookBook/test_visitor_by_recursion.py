#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,sys

'''
有时候会构建一个由大量不同对象组成的数据结构。 假设你要写一个表示数学表达式的程序，那么你可能需要定义如下的类：
'''

class Node:
	pass

# 针对操作数将可执行操作进行分类
class UnaryOperator(Node):
	'''
	单目运算
	'''
	def __init__(self,operand):
		self.operand = operand

class BinaryOperator(Node):
	'''
	二元运算
	'''
	def __init__(self,left,right):
		self.left = left
		self.right = right

class Number(Node):
	'''
	取值运算
	'''
	def __init__(self,value):
		self.value = value

# 封装具体操作
class Add(BinaryOperator):
	pass

class Sub(BinaryOperator):
	pass

class Mul(BinaryOperator):
	pass

class Div(BinaryOperator):
	pass

class Negate(UnaryOperator):
	pass


def test_node():
	#  1 + 2 * (3 - 4) / 5 手动实现运算公式
	t1 = Sub(Number(3),Number(4))
	t2 = Mul(Number(2),t1)
	t3 = Div(t2,Number(5))
	t4 = Add(Number(1),t3)

'''
这样做的问题是对于每个表达式，每次都要重新定义一遍，有没有一种更通用的方式让它支持所有的数字和操作符呢。 这里我们使用访问者模式可以达到这样的目的
'''

class NodeVisitor:
	'''
	提供访问节点，反射执行操作路由功能
	'''
	def visit(self,node):
		methname = 'visit_'+type(node).__name__ # 基于类型区分操作
		meth = getattr(self,methname,None) # 反射获取据图操作方法
		if meth is None: # 异常处理
			meth = self.generic_visit
		return meth(node)
	
	def generic_visit(self,node):
		raise RuntimeError('No {} method'.format('visit_'+type(node).__name__))
	
class Evalutor(NodeVisitor):
	'''
	访问节点具体实现
	'''
	def visit_Number(self,node):
		return node.value
	
	def visit_Add(self,node):
		return self.visit(node.left) + self.visit(node.right)

	def visit_Sub(self,node):
		return self.visit(node.left) - self.visit(node.right)
	
	def visit_Mul(self,node):
		return self.visit(node.left) * self.visit(node.right)
	
	def visit_Div(self,node):
		return self.visit(node.left) / self.visit(node.right)
	
	def visit_Negate(self,node):
		return - node.operand

def test_elevator():
	#  1 + 2 * (3 - 4) / 5 手动实现运算公式
	t1 = Sub(Number(3),Number(4))
	t2 = Mul(Number(2),t1)
	t3 = Div(t2,Number(5))
	t4 = Add(Number(1),t3)
	
	
	e = Evalutor()
	res = e.visit(t4) # 逐层递归向下检索，直到获取底层最基本元素，执行基础运算，再逐层返回
	print(res)
	
	print(sys.getrecursionlimit()) # 1000 当前系统支持最大递归深度 1000
	
	a= Number(0)
	for x in range(1,1001): # 超过递归深度，溢出
		a = Add(a,Number(x))
	e.visit(a) # RecursionError: maximum recursion depth exceeded while calling a Python object
	


'''
作为一个不同的例子，下面定义一个类在一个栈上面将一个表达式转换成多个操作序列：
'''
class StackCode(NodeVisitor):
	def generate_code(self,node):
		self.instructions = []
		self.visit(node)
		return self.instructions

	def visit_Number(self,node):
		self.instructions.append(('PUSH',node.value))
	
	'''
	使用访问者模式通过父类 NodeVisitor 中的 visit() 调用系统的  getatt() 函数实现递归访问功能，避免大量 if/else语句
	'''
	def binop(self,node,instruction):
		self.visit(node.left)
		self.visit(node.right)
		self.instructions.append(instruction)
	
	def visit_Add(self,node):
		self.binop(node,'ADD')
	
	def visit_Sub(self,node):
		self.binop(node,'SUB')
	
	def visit_Mul(self,node):
		self.binop(node,'MUL')
	
	def visit_Div(self,node):
		self.binop(node,'DIV')
	
	def unaryop(self,node,instruction):
		self.visit(node.operand)
		self.instructions.append((instruction,))
	
	def visit_Negate(self,node):
		self.unaryop(node,'NEG')
	

def test_stack_cal():
	#  1 + 2 * (3 - 4) / 5 手动实现运算公式
	t1 = Sub(Number(3),Number(4))
	t2 = Mul(Number(2),t1)
	t3 = Div(t2,Number(5))
	t4 = Add(Number(1),t3)
	
	s = StackCode()
	stacks = s.generate_code(t4)
	print(stacks)
	
	[('PUSH', 1), ('PUSH', 2), ('PUSH', 3), ('PUSH', 4), 'SUB', 'MUL', ('PUSH', 5), 'DIV', 'ADD']
	
	
	
	

'''
还有一点需要指出的是，这种技术也是实现其他语言中switch或case语句的方式。 比如，如果你正在写一个HTTP框架，你可能会写这样一个请求分发的控制器：
'''
class HTTPHandler:
	def handler(self,request):
		methname = 'do_' + request.request_method
		getattr(self,methname)(request) # 基于http 请求体，请求函数表征，通过反射，调用相应方法处理请求
	
	def do_GET(self,request):
		print('do_get')
	
	def do_POST(self,request):
		print('do_post')
	
	def do_HEAD(self,request):
		print('do_head')
		

		

if __name__=="__main__":
	try:
		test_elevator()
		# test_stack_cal()
		
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




