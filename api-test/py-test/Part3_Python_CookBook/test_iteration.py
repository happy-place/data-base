#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""

import os,traceback
from collections import deque
import itertools
from itertools import permutations,combinations
from collections import defaultdict


def manual_iter():
	# 手动迭代，触发异常终止
	# with open('/etc/passwd') as f:
	# 	try:
	# 		while True:
	# 			line = next(f)
	# 			print(line, end='\n') # print 中的 end 分割符只能在 python 3.x 中使用
	# 	except StopIteration:
	# 		pass
	
	# 手动迭代，获取不成功时，返回None终止
	with open('/etc/passwd') as f:
		while True:
			line = next(f,None)
			if line:
				# print 中的 end 分割符只能在 python 3.x 中使用，通过定义 end 可将默认的\n 行分割符抹去，上下行间不存在空白行
				print(line, end=' ')
			else:
				break
	
def test_list():
	items = [1,2,3]
	it = iter(items)
	
	print(next(it)) # 1
	print(next(it)) # 2
	print(next(it)) # 3
	print(next(it)) # StopIteration

class Node:
	'''
	创建包含 __iter__(self)方法的对象，此类对象被称为可迭代对象
	'''
	def __init__(self,value):
		self._value = value
		self._children = []
	
	# toString()
	def __repr__(self):
		return 'Node({!r})'.format(self._value)

	def add_child(self,node):
		self._children.append(node)
	
	def __iter__(self):
		return iter(self._children)

class DepthFirstNode(Node):
	def depth_first(self):
		yield self
		for c in self:
			yield from c.depth_first()
	


class DepthFirstIterator(object):
	def __init__(self,start_node):
		self._node = start_node
		self._children_iter = None # 子集子集迭代器
		self._child_iter = None # 孩子子集迭代器
	
	def __iter__(self):
		return self
	
	def __next__(self):
		# 1起始点，自己的迭代器为空，需要将自己封装到 iter() 赋值给子集迭代器抛出
		if self._children_iter is None:
			self._children_iter = iter(self._node)
			return self._node
		elif self._child_iter: # 2第二次时 孩子迭代器为空 跳过
			try:
				nextchild = next(self._child_iter) # 4 当前子节点的孩子节点迭代完毕，抛出下一个子节点，并且此时孩子节点迭代器为空
				return nextchild
			except StopIteration:
				self._child_iter = None
				return next(self)
		else: # 3子集迭代器第一次迭代，将子节点的 封装到孩子迭代器中返回，本地迭代拿到子节点，下次就从改子节点的孩子节点开始迭代
			self._child_iter = next(self._children_iter).depth_first() # 5将下一个子节点的孩子节点抛出
			return self

class DepthFirstNode2(Node):
	def depth_first(self):
		return DepthFirstIterator(self)



def test_proxy_iter():
	root = Node(0)
	child1 = Node(1)
	child2 = Node(2)
	root.add_child(child1)
	root.add_child(child2)
	
	for ch in root:
		print(ch)

def test_depth_first_iter():
	# root = DepthFirstNode(0)
	# child1 = DepthFirstNode(1)
	# child2 = DepthFirstNode(2)
	#
	# root.add_child(child1)
	# root.add_child(child2)
	#
	# child11 = DepthFirstNode(11)
	# child12 = DepthFirstNode(12)
	# child1.add_child(child11)
	# child1.add_child(child12)
	#
	# child21 = DepthFirstNode(21)
	# child2.add_child(child21)
	#
	# for c in root.depth_first():
	# 	print(c)
	
	root = DepthFirstNode2(0)
	child1 = DepthFirstNode2(1)
	child2 = DepthFirstNode2(2)
	
	root.add_child(child1)
	root.add_child(child2)
	
	child11 = DepthFirstNode2(11)
	child12 = DepthFirstNode2(12)
	child1.add_child(child11)
	child1.add_child(child12)
	
	child21 = DepthFirstNode2(21)
	child2.add_child(child21)
	
	for c in root.depth_first():
		print(c)


class ReversableCountDown:
	def __init__(self,start):
		self.start=start
		
	def __iter__(self):
		n = self.start
		while n >0:
			yield n 
			n -=1
	
	def __reversed__(self):
		n = 1
		while n <= self.start:
			yield n
			n +=1
		
def test_reversed_iter():
	'''
	反向迭代
	:return:
	'''
	# 对应没有实现 __reversed__() 的函数通过借助 reversed(list())机制进行逆转 (注：会消耗大量内存)
	# a = [1,2,3,4]
	# for x in reversed(a):
	# 	print(x)
	
	for rr in reversed(ReversableCountDown(5)): # 1~5
			print(rr)
		
	for rr in ReversableCountDown(5): # 5~1
		print(rr)

# 通过生成器创建可迭代对象
def create_iterator_by_generator(start,end,increment):
	while start <= end:
		yield start  # yield 关键字存在的函数为生成器函数，yield 相当于return, 会先将后面内容压入方法栈，然后执行带底层，在返回
		start +=increment

def countdown(n):
	print('start to count from {n}'.format(n = n))
	while n>0:
		yield n
		n -= 1
	# ----------以上在正常迭代是输出，以下在迭代结束时执行----------------
	print('Done!')

class linehistory:
	'''
	可存储状态迭代器
	获取截止到目标位置前，最近3行
	'''
	def __init__(self,lines,hislen = 3):
		self.lines = lines
		self.history = deque(maxlen=hislen)
	
	def __iter__(self):
		for lineno,line in enumerate(self.lines,1):
			self.history.append((lineno,line))
			yield line
	
	def clear(self):
		self.history.clear()

def test_stateful_iter():
	with open('parser.out','r') as f :
		lines = linehistory(f)
		for line in lines:
			if 'Rule 4' in line:
				for lineno,hline in lines.history:
					print('{lineno}:{hline}'.format(lineno=lineno,hline=hline),end='')
	'''
	7:Rule 2     expr -> expr MINUS term
	8:Rule 3     expr -> term
	9:Rule 4     term -> term TIMES factor
	
	'''

def test_iter_slices():
	'''
	正常情况下迭代器没有切片操作，通过itertools.isclice() 可对迭代器使用切片
	迭代器和生成器不能使用标准的切片操作，因为它们的长度事先我们并不知道 (并 且也没有实现索引)。函数 islice()
	返回一个可以生成指定元素的迭代器，它通过遍 历并丢弃直到切片开始索引位置的所有元素。然后才开始一个个的返回元素，并直到切 片结束索引位置。
	这里要着重强调的一点是 islice() 会消耗掉传入的迭代器中的数据。必须考虑到 迭代器是不可逆的这个事实。所以如果你需要之后再次访问这个迭代器的话，
	那你就得 先将它里面的数据放入一个列表中。
	:return:
	'''
	for c in itertools.islice(ReversableCountDown(30),10,20):
		print(c)
		

def test_dropwhile():
	# with open('/etc/passwd','r') as f:
	# 	# 过滤掉以 # 开头的内容，其余打印输出
	# 	for line in itertools.dropwhile(lambda s:s.startswith("#"),f):
	# 		print(line)
	# 	f.close()

	items = ['a','b','c',1,3,5,6]
	# 从第三个元素开始迭代，以None表示追到末尾，islice(items,3,5) 表示输出 items[3,5) 间元素
	for x in itertools.islice(items,3,None):
		print(x)

def test_permutations():
	items = ['a','b','c']
	# 排列有顺序 如：(a,c) 和 (c,a) 是两种选项
	for p in permutations(items): # 默认所有元素参与排列 A(3,3) 3*2*1
		print(p)
		'''
		('a', 'b', 'c')
		('a', 'c', 'b')
		('b', 'a', 'c')
		('b', 'c', 'a')
		('c', 'a', 'b')
		('c', 'b', 'a')
		'''
	print('-------')
	
	for p in permutations(items,2): # 选两个元素进行排列组合 A(2,3) 3*2
		print(p)
		'''
		('a', 'b')
		('a', 'c')
		('b', 'a')
		('b', 'c')
		('c', 'a')
		('c', 'b')
		'''
	print('-------')
	
	# 组合无序，如：(a,c) 和 (c,a) 是同一种选项
	for c in combinations(items,2): # 选两个元素进行排列组合 C(2,3) 3*2*1/2*1 = 3
		print(c)
		'''
		('a', 'b')
		('a', 'c')
		('b', 'c')
		'''
	print('-------')
	
	# 允许放回排序 3个空位，没个空位都有三种选择：C(3,3) 三个全部一样 + C(2,3)两个全部一样 + C(1,3)三个全部不同 = 9
	for c in itertools.combinations_with_replacement(items,3):
		print(c)
		'''
		('a', 'a', 'a')
		('a', 'a', 'b')
		('a', 'a', 'c')
		('a', 'b', 'b')
		('a', 'b', 'c')
		('a', 'c', 'c')
		('b', 'b', 'b')
		('b', 'b', 'c')
		('b', 'c', 'c')
		('c', 'c', 'c')
		
		'''

def get_index_form_iter():
	'''
	遍历集合时借助enumerate 带出索引
	:return:
	'''
	my_list = ['a','b','c']
	for idx,val in enumerate(my_list):
		print(idx,val)
	'''
	0 a
	1 b
	2 c
	'''

def trace_error():
	'''
	借助 enumerate 返回行号特征，追踪异常值
	:return:
	'''
	with open('num.txt','r') as f:
		count = 0
		for lineno,line in enumerate(f,1):
			fields = line.split(" ")
			try:
				int(fields[1])
			except ValueError as e:
				count +=1
				print('【ERROR-{cnt}】line {lineno}: parse error: {line}'.format(cnt=count,lineno=lineno,line=line))
				
		f.close()


def reverse_index():
	'''
	统计文本中，单词出现行号
	:return:
	'''
	words_summary = defaultdict(list)
	with open('test_bytearr.py','r') as f:
		for lineno,line in enumerate(f,1):
			words = (word.strip().lower() for word in line.split()) # split 默认以空格为分割符
			for word in words:
				words_summary[word].append(lineno)
	print(words_summary)
	'''
    defaultdict(<class 'list'>, {'#!/usr/bin/env': [1], 'python': [1], '#': [2, 14, 16, 16, 17, 18, 22, 23, 24, 38, 43, 44, 45, 46, 57, 59, 60, 68, 69, 70, 71], '-*-': [2, 2],
    '''
	
def loop_tuple():
	data = [(1,2),(3,4),(4,5)]
	for n,(x,y) in enumerate(data):
		print(n,x,y)
		'''
		0 1 2
		1 3 4
		2 4 5
		'''


if __name__=="__main__":
	try:
		# manual_iter()
		# test_list()
		# test_proxy_iter()
		
		# for x in create_iterator_by_generator(0,4,0.5):
		# 	print(x)
		
		# cd = countdown(3)
		# print(next(cd)) # 3
		# print(next(cd)) # 2
		# print(next(cd)) # 1
		# print(next(cd)) # Done StopIteration
		
		# test_depth_first_iter()
		
		# test_reversed_iter()
		
		# test_stateful_iter()
		
		# test_iter_slices()
		
		# test_dropwhile()
		
		# test_permutations()
		
		# get_index_form_iter()
		
		# trace_error()
		
		# reverse_index()
		
		loop_tuple()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)



