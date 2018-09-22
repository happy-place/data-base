#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback
import heapq

class PriortyQueue:
	def __init__(self):
		self._queue = []
		self._index = 0
	def push(self,item,priroity):
		'''往内置_queue 中插入item 对象，并维护插入顺序_index 和 优先级 priroity（此处取优先级大的，因此取负数）,
		如果单纯使用 priroity 优先级维护插入和弹出顺序的话，当优先级一致时，就无法执行插入了，会报错，因此还需要维护自增索引。
		优先级不同 从大到小，优先级相同，按插入顺序先进先出
		'''
		heapq.heappush(self._queue,(-priroity,self._index,item))
		self._index +=1

	def pop(self):
		return heapq.heappop(self._queue)[-1]

class Item:
	def __init__(self,name):
		self.name = name
		
	def __repr__(self):  # 覆写 __repr__ 相当于定制 toString()
		# return 'Item({!s})'.format(self.name) >> Item(bar)
		# return 'Item({!r})'.format(self.name) >> Item('bar') !r 调用的是 repr() 取得失标准字符展示形式
		return 'Item({!s})'.format(self.name)
	


def test_heapq_list(*nums):
	'''
	获取 top-n ，当待取出数据集合远小于总集合时，可以使用 heapq nlargest nsmallest 进行堆内排序
	如果二者接近，则不适合 heapq 取值了，直接使用 sorted(items)[:n] 或 sorted(items)[-n:] 取值即可
	
	:param nums:
	:return:
	'''
	# nums 在定义函数时就被声明成为了list，因此直接具备 list 属性
	print(heapq.nlargest(2,nums))  # 最大的2个
	print(heapq.nsmallest(2,nums)) # 最小的2个


def test_heapq_dict(*args):
	cheap = heapq.nlargest(3,args,key=lambda a:a['price']) # 按指定的取key 方式取出key进行排序
	expensive = heapq.nsmallest(3,args,key=lambda a:a['price'])
	print(cheap)
	print(expensive)


def test_heapify():
	nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
	heap = list(nums)
	heapq.heapify(heap)
	print(heap) # [-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8] 堆底heap[0]元素必须是最小的，其余顺序可错乱
	
	v = heapq.heappop(heap) # -4 heappop 弹出堆底元素
	print(v)
	v = heapq.heappop(heap) # 1
	print(v)
	v = heapq.heappop(heap) # 2
	print(v)

if __name__=="__main__":
	try:
		# print_stack()
		# test_q()
		# test_pop()
		
		# nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
		# test_heapq_list(*nums) # def test_heapq(*nums) 接受不定参数，传参是时必须将集合解封
		#
		# portfolio = [
		# 	{'name': 'IBM', 'shares': 100, 'price': 91.1},
		# 	{'name': 'AAPL', 'shares': 50, 'price': 543.22},
		# 	{'name': 'FB', 'shares': 200, 'price': 21.09},
		# 	{'name': 'HPQ', 'shares': 35, 'price': 31.75},
		# 	{'name': 'YHOO', 'shares': 45, 'price': 16.35},
		# 	{'name': 'ACME', 'shares': 75, 'price': 115.65}
		# 	]
		# test_heapq_dict(*portfolio)
		
		# test_heapify()
		
		# 优先级不同，从大到小，优先级相同，先进先出
		q = PriortyQueue()
		q.push(Item('foo'),1) # 3
		q.push(Item('bar'),5) # 1
		q.push(Item('spam'),4) # 2
		q.push(Item('grok'),1) # 4
		
		v = q.pop()
		print(v)
		v = q.pop()
		print(v)
		v = q.pop()
		print(v)
		v = q.pop()
		print(v)
		
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
