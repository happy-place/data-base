#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,html,math,logging
from functools import partial
from multiprocessing import Pool
from socketserver import StreamRequestHandler,TCPServer
from urllib.request import urlopen



def avg(first,*rest):
	'''
	可变参数
	:param first:
	:param rest:
	:return:
	'''
	return (first+sum(rest)) / (1+len(rest))


def make_element(name,value,**attrs): # 接受dict
	keyvals = [' %s="%s"' % item for item in attrs.items()] # 直接填充kv
	attr_str = ''.join(keyvals) # 拼接
	element = '<name{attr}>{value}</name>'.format(name=name,attr=attr_str,value = html.escape(value)) # 逃逸展示
	return element


def anyargs(*args,**kwargs):
	print(type(args)) # <class 'tuple'>
	print(type(kwargs)) # <class 'dict'>


def test_order(a,b=1,*c,**d):
	print('a 位置参数，必须传入')
	print('b 为关键入参，有默认值，可以不传')
	print('c 为dict，关键参数a之后，位置参数前后都行，并在**d 之前')
	print("**d必须在最后")


def recv(maxsiez,*,block):
	'''
	强制必须显示传入关键字入参，可将次关键字放在 * 或 *c 之后
	
	:param maxsiez:
	:param block:
	:return:
	'''
	print(maxsiez,block)


def minium(*values,clip=None):
	m = min(values)
	if clip is not None:
		m = clip if clip < m else m
	return m


def add(x:int,y:int) -> float:
	'''
	添加入参和返回值得函数参数注解，增加程序可读性,注释只是提示作用，并不会形成约束
	
	:param x:
	:param y:
	:return:
	'''
	return x+y


def myfunc():
	'''
	返回元祖
	:return:
	'''
	return 1,2,3


def test_tuple():
	'''
	快速声明元祖
	'''
	a = (1,2)
	b = 1,2
	print(a,b) # (1, 2) (1, 2)
	

def spam(a,b=24):
	print(a,b)

def spam2(a,b='empty'):
	# 通过观察默认值有没有被修改来判断是否传入了相应参数
	if b == 'empty':
		print('No b value supplied')
	print(a)


def spam3(a,b=[]):
	print(b)
	return b

def test_spam3():
	k = spam3(1)
	k.append(12)
	print(k)
	z = spam3(10)
	z.append('hello')
	print(k)
	# 不想对list传值，需要置空 None,否则多次调用间会形成串联
	'''
	[]
	[12]
	[12]
	[12, 'hello']
	'''

def test_lambda():
	add = lambda x,y:x+y
	print(add(2,3))
	
	print(add('hello ','world'))
	
	names = ['David Beazley', 'Brian Jones', 'Raymond Hettinger', 'Ned Batchelder']
	print(sorted(names,key=lambda name:name.split()[-1].lower())) # 尾部字母小写排序

def test_wrap():
	x = 10
	a = lambda y:x+y
	x = 20
	b = lambda y:x+y
	
	# 调用时，再入参
	print(a(10))
	print(b(30))
	
	x = 10
	c = lambda y,x=x:x+y # 10+y
	x= 20
	d = lambda y,x=x:x+y # 20+y
	print(c(10))
	print(d(20))

	funcs = [lambda x:x+n for n in range(4)] # 真正调用时，再装配n
	for f in funcs:
		print(f(0))
		'''
		3
		3
		3
		3
		'''
		
	funcs = [lambda x,n=n:x+n for n in range(4)] # 创建匿名函数时，就绑定了n
	for f in funcs:
		print(f(0))
		'''
		0
		1
		2
		3
		'''

def spamn(a,b,c,d):
	print(a,b,c,d)

def test_partial():
	s1 = partial(spamn,1) # 将a固定为1,按顺序固定
	s1(2,3,4)
	s2 = partial(spamn,1,2)
	s2(3,4)
	s2 = partial(spamn,d=4) # 通过关键参数进行固定
	s2(1,2,3)

def get_distince(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	return(math.hypot(x2-x1,y2-y1)) # 1.4142135623730951
	
def output_result(result,log=None):
	if log is not None:
		log.debug('Got %r',result)

def add(x,y):
	return x+y

class EchoHandler(StreamRequestHandler):
	def __init__(self,*args,ack,**kwargs):
		self.ack = ack
		super().__init__(*args,**kwargs)
	
	def handle(self):
		for line in self.rfile:
			self.wfile.write(b'GOT:'+line)


class EchoHandler2(StreamRequestHandler):
	def __init__(self,*args,ack,**kwargs): # 强制关键参数，ack
		self.ack = ack
		super().__init__(*args,**kwargs)
	
	def handle(self):
		for line in self.rfile:
			self.wfile.write(b'GOT:'+line)


def test_tcp():
	serv = TCPServer(('',15000),EchoHandler)
	serv.serve_forever()

def partial_init():
	serv = TCPServer(('',15000),partial(EchoHandler2,ack=b'RECEIVED'))
	serv.serve_forever()

class UrlTemplate:
	def __init__(self,template):
		self.templpate = template
	
	def open(self,**kwargs):
		'''
		通过闭包将单个方法的类转换成为函数
		
		:param kwargs:
		:return:
		'''
		return urlopen(self.templpate.format_map(kwargs))


def test_urltemplate():
	yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
	for line in yahoo.open(names='IBM,AAPL,Fb',fields ='sl1c1v'):
		print(line.decode())



# 装饰器
def urltemplate(template):
	def opener(**kwargs):
		req = template.format_map(kwargs) # 自动填充kv
		print(req)
		return urlopen(req)
	return opener





if __name__=="__main__":
	try:
		# print(avg(1,2))
		# print(avg(1,2,3))
		# print(make_element('item','Albatross',size='large',quantity=6)) # <name size="large" quantity="6">Albatross</name>
		# print(make_element('p','<spam>')) # <name>&lt;spam&gt;</name>
		#
		# anyargs()
	
		# test_order(1)
		#
		# recv(1,block=3) # 强制关键参数可读性更好,比help 更好
		
		# print(help(recv))
		'''
		recv(maxsiez, *, block)
	    强制必须显示传入关键字入参，可将次关键字放在 * 或 *c 之后
	    
	    :param maxsiez:
	    :param block:
	    :return:
		'''
		# print(minium(1,4,-3,2,10))
		# print(add(1,2))
		# print(help(add))
		
		# print(add.__annotations__) # {'x': <class 'int'>, 'y': <class 'int'>, 'return': <class 'float'>}
		# a,b,c = myfunc()
		# print(a,b,c)
		# test_tuple()
		
		# spam(1) # 使用默认值
		# spam(1,5) # 覆盖默认值
		
		# spam2(2)
		# spam2(2,None) # 即便传入None,在此也是传入了值了的
		
		# test_spam3()
		
		# test_lambda()
		
		# test_wrap()
		# test_partial()
		# get_distince((1,1),(2,2))
		#
		# points = [(1,2),(3,4),(5,6),(7,8)]
		# target = (4,3)
		# points.sort(key=partial(get_distince,target)) # 按所有点到目标点 target 的距离进行排序
		# print(points)
		
		# # 自定义log对象
		# logging.basicConfig(level=logging.DEBUG)
		# log = logging.getLogger('test')
		#
		# # 声明进程池
		# p = Pool()
		# # 使用进程池异步调用 add(3,4) 结果回调传给偏函数 partial(output_result,log=log)
		# # 借助偏函数预先组织回调函数
		# # p.apply_async(add,(3,4),callback=partial(output_result,log=log))
		# p.apply_async(add,(3,4),callback=lambda result:output_result(result,log)) # 偏函数往往可以被lambda 取代
		#
		# p.close() # 关闭进程队列，不允许添加新任务
		# p.join() # 启动多进程
		
		
		tremplate = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
		tremplate(names='IBM,AAPL,Fb',fields ='sl1c1v')
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




