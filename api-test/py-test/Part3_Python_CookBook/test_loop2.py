#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""

import os,traceback

def display(a):
	l = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
	print([l[a[i]] for i in range(len(a))])


def backtracking(n, m, check, handle):
	def dfs(a, k):
		for i in range(n):
			a[k] = i
			if check(a, k):
				if k == m - 1:
					handle(a)
				else:
					dfs(a, k + 1)
	a = [0 for _ in range(m)]
	dfs(a, 0)


def counter(n, m):
	backtracking(n, m, lambda a, k: True, lambda a: print(a))


def permutation(n, m):
	def check(a, k):
		for i in range(k):
			if a[i] == a[k]:
				return False
		return True
	backtracking(n, m, check, display)


def combination(n, m):
	def check(a, k):
		for i in range(k):
			if a[i] >= a[k]:
				return False
		return True
	backtracking(n, m, check, display)


def nqueen(n):
	def check(a, k):
		for i in range(k):
			if a[i] == a[k] or abs(a[i] - a[k]) == k - i:
				return False
		return True
	backtracking(n, n, check, lambda a: print(a))


if __name__=="__main__":
	try:
		# print("counter =>")
		# counter(6, 3)
		
		# print("permutation =>")
		# permutation(6, 3)
		#
		# print("combination =>")
		# combination(6, 3)
		#
		print("nqueen =>")
		nqueen(4)
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




