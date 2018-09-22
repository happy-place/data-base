#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,ast


def test_ast():
	ex = ast.parse('2 + 3*4 + x',mode='eval')
	print(ex) # <_ast.Expression object at 0x102913cc0>
	print(ast.dump(ex))
	'''
	Expression(body=BinOp(left=BinOp(left=Num(n=2), op=Add(), right=BinOp(left=Num(n=3), op=Mult(), right=Num(n=4))), op=Add(), right=Name(id='x', ctx=Load())))
	'''
	
	top = ast.parse('for i in range(10): print(i)',mode='exec')
	print(top) # <_ast.Module object at 0x102934f98>
	
	print(ast.dump(top))
	'''
	Module(body=[For(target=Name(id='i', ctx=Store()), iter=Call(func=Name(id='range', ctx=Load()), args=[Num(n=10)], keywords=[]), body=[Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Name(id='i', ctx=Load())], keywords=[]))], orelse=[])])
	'''
	
class CodeAnalyzer(ast.NodeVisitor):
	def __init__(self):
		self.loaded = set()
		self.stored = set()
		self.deleted = set()
	
	def visit_Name(self,node):
		if isinstance(node.ctx,ast.Load):
			self.loaded.add(node.id)
		elif isinstance(node.ctx,ast.Store):
			self.stored.add(node.id)
		elif isinstance(node.ctx,ast.Del):
			self.deleted.add(node.id)


def test_code_analyzer():
	code = '''for i in range(10):print(i);del i'''
	
	top = ast.parse(code.replace('	',''),mode='exec')
	c = CodeAnalyzer()
	c.visit(top)
	print('Loaded: ',c.loaded) # Loaded:  {'print', 'range', 'i'}
	print('Stored: ',c.stored) # Stored:  {'i'}
	print('Deleted: ',c.deleted) # Deleted:  {'i'}
	
	exec(compile(top,'<stdin>','exec')) # 编译执行
	
	
	
	
	
	
	

if __name__=="__main__":
	try:
		# test_ast()
		test_code_analyzer()
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




