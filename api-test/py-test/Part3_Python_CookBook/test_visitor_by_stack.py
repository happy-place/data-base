#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,types

'''
不用递归实现访问者模式

这一小节我们演示了生成器和协程在程序控制流方面的强大功能。 避免递归的一个通常方法是使用一个栈或队列的数据结构。
 例如，深度优先的遍历算法，第一次碰到一个节点时将其压入栈中，处理完后弹出栈。visit() 方法的核心思路就是这样。



'''

# 定义基础节点
class Node:
	pass

# 操作数层面归类
class UnaryOperator(Node):
	def __init__(self,operand):
		self.operand = operand
		
class BinaryOperator(Node):
	def __init__(self,left,right):
		self.left = left
		self.right = right

# 针对操作数定制具体操作实现类，此处只是基础操作的替代，真实的操作执行还是依赖系统底层操作
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

class Number(Node):
	def __init__(self,value):
		self.value = value

# 遍历节点访问者
class NodeVisitor:
	def visit(self,node):
		stack = [node] # 取当前节点存如列表
		last_result = None # 暂时将上一步操作结果记为 空
		while stack:
			try:
				last = stack[-1] # 取出自己
				if isinstance(last,types.GeneratorType): # 如果是生成器
					stack.append(last.send(last_result))# 就将生成器往前拨动一步
					last_result = None
				elif isinstance(last,Node): # 如果是具体可执行节点，就执行访问操作，并将访问结果压栈
					stack.append(self._visit(stack.pop()))
				else:
					last_result  =stack.pop() # 压到最底层，开始吐结果
			except StopIteration:
				stack.pop() # 迭代终止，吐出最后结果
		return last_result
	
	def _visit(self,node):
		methname = 'visit_'+type(node).__name__
		meth = getattr(self,methname,None)
		if meth is None:
			meth = self.generic_visit # 异常
		return meth(node)
	
	def generic_visit(self,node):
		raise RuntimeError('No {} method'.format('visit_'+type(node).__name__))
	

	
class Evaluator(NodeVisitor):
	def visit_Number(self,node):
		return node.value
	'''
	所有访问操作全部通过迭代策略，推进，防止递归越界
	'''
	def visit_Add(self,node):
		# return self.visit(node.left) + self.visit(node.right) # 单个函数调用有递归深度限制 1000，
		# 但如果改造成 (yield node.left) + (yield node.right) 左侧 调用完毕，会将程序控制权交给右侧，然后汇总结果。
		yield (yield node.left) + (yield node.right)
	
	def visit_Sub(self,node):
		yield (yield node.left) - (yield node.right)
	
	def visit_Mul(self,node):
		yield (yield node.left) * (yield node.right)
	
	def visit_Div(self,node):
		yield (yield node.left) / (yield node.right)
	
	def visit_Negate(self,node):
		yield - (yield node.operand)
		
		
def test_visitor():
	a = Number(0)
	for x in range(1,1001):
		a = Add(a,Number(x)) # 500500
	
	e = Evaluator()
	res = e.visit(a)
	print(res)
	




if __name__=="__main__":
	try:
		test_visitor()
		
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




