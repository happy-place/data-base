#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""


import os,traceback,heapq

def test_merge():
	a = [1,4,7,2]
	b = [3,4,1,2]
	# 已经排好序的集合通过 headp.merge 合并后，仍能够进一步在merge过程中进行排序
	for x in heapq.merge(sorted(a),sorted(b)):
		print(x)

def merge_file():
	'''
	heapq.merge 在具备d迭代器特征，不会立即读取所有序列，因此可以在非常长的文件序列中使用到它，而且内存开销不会太大
	合并文件特点： 内容相同，位置相同的行按先后顺序联排，其余按序排
	:return:
	'''
	with open('test_heapq.py','r') as in1 ,\
		open('test_from_bytes.py','r') as in2 , \
		open('test_itemgetter.py','r') as in3 , \
		open('merged.txt','w') as out:
		for line in heapq.merge(in1,in2,in3):
			out.write(line)
	



if __name__=="__main__":
	try:
		# test_merge()
		merge_file()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)





