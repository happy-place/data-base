#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback
from collections import deque
import heapq


def search(lines, pattern, history=5):
	previous_lines = deque(maxlen=history) # 轮询覆盖队列
	for line in lines:
		if pattern in line:
			yield line, previous_lines # 每次执行完下面的 append 后，进行返回 yeild 在此处相当于 return ，返回时本次line 和 历史line
		previous_lines.append(line)


def print_stack():
	with open('test.txt','r') as f:
		for line, prevlines in search(f, 'python', 5): # 每往下读一行，都会把历史数据全部消费一次
			for pline in prevlines:
				print(pline, end='')
				print(line, end='')
				print('-' * 20)
		
				
def test_q():
	q = deque(maxlen=3) # 超过3个就会自行弹出
	q.append(1)
	q.append(2)
	q.append(3)
	print(q)  # deque([1, 2, 3], maxlen=3)
	q.append(4)
	print(q) # deque([2, 3, 4], maxlen=3)
	
def test_pop():
	'''
	在队列头或尾插入或删除元素，复杂度都是o(N),在列表头插入或删除元素时间复杂度都为 o(N)
	原因：队列借助链表实现，只需要修改一个节点就可维持顺序，列表借助数组实现，每次在头部插入或删除，都需要整体平移
	:return:
	'''
	q = deque() # 没设置maxlen时，可无限膨胀
	q.append(1) # 默认从右侧添加
	q.append(2)
	q.append(3)
	print(q) # deque([1, 2, 3])
	q.appendleft(4) # deque([4, 1, 2, 3]) 头部添加
	
	print(q)
	# e = q.pop() # 默认从右侧弹出
	e = q.popleft() # 从左侧弹出
	print(e,q)




if __name__=="__main__":
	try:
		# print_stack()
		# test_q()
		test_pop()
		
		
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)


