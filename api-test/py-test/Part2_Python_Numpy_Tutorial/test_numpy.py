#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/17'
Info:
        
"""

import sys,os
if sys.version_info[0] !=2:
	print("【WARN】numpy need python2.x .")
	sys.exit(0)
else:
	import numpy as np

if __name__=="__main__":
	try:
		# 单维度
		a = np.array([1,2,3])
		print(type(a)) # <type 'numpy.ndarray'>
		
		print(a.shape) # 打印规格 列 x 行 (3,)
		
		print(a[0],a[1],a[2]) # (1, 2, 3)
		
		a[0] = 5 # 赋值修改
		print(a)
		
		# 多维
		b = np.array([[1,2,3],[4,5,6]])  # (2, 3) 两列三行
		print(b.shape)
		print(b[0,0],b[0,1],b[1,0])
		
		# zero one
		a = np.zeros((2,2)) # 2列2行 全部为0
		print(a)
		'''
		[[ 0.  0.]
        [ 0.  0.]]
		'''
		
		b = np.ones((1,2))  # 1列2行 全部为1
		print(b)
		'''
		[[ 1.  1.]]
		'''
		
		c = np.full((2,2),7) # 2列2行，全部使用7填充
		print(c)
		'''
		[[ 7.  7.]
        [ 7.  7.]]
		'''
		
		d = np.eye(2) # 对称矩阵,整对角线元素个数为2，其余为0
		print(d)
		'''
		[[ 1.  0.]
        [ 0.  1.]]
		'''
		
		e = np.random.random((2,2)) # 2列2行 元素为 0~1 直接随机数
		print(e)
		'''
		[[ 0.36144624  0.19257374]
        [ 0.84059367  0.22159741]]
		'''
		
		# 切片操作
		a = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
		b = a[:2,1:3] # 取 [0,2) 行，[1,3) 列切片
		print(a)
		print(b)
		'''
		      ------
		[[ 1 | 2  3 | 4]
         [ 5 | 6  7 | 8]
              ------
         [ 9 10 11 12]]
         
        [[2 3]
         [6 7]]
		'''
		
		print(a[0,1]) # 0列1行位置元素 2
		
		b[0,0] = 77 # b 是 a 的子集，b 中元素变化，a 也变化，传地址
		print(a)
		
		# 子集
		a = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
		row_r1 = a[1,:]  # 取第一列全部元素，单维
		row_r2 = a[1:2,:] # 取[1,2)列，全部元素，二维
		print(row_r1,row_r1.shape) # (array([5, 6, 7, 8]), (4,))
		print(row_r2,row_r2.shape) # (array([[5, 6, 7, 8]]), (1, 4))
		
		col_r1 = a[:,1] # 取 第1行全部元素，单维
		col_r2 = a[:,1:2] # 取第[1,2)行全部元素，二维
		print(col_r1,col_r1.shape) # (array([ 2,  6, 10]), (3,))
		print(col_r2,col_r2.shape) # (array([[ 2],[ 6],[10]]), (3, 1))
		
		a = np.array([[1,2],[3,4],[5,6]])
		print(a[[0,1,2],[0,1,0]]) # 取(0,0) 1 (1,1) 4 (2,0) 5 位置元素
		
		print(np.array([a[0,0],a[1,1],a[2,0]])) # 1列3行 [1 4 5]
		
		print(a[[0,0],[1,1]]) # 取(0,1) (0,1) 元素，组合成1列2行
		
		a = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
		print(a,a.shape) # a.shape (4,3) 二维
		'''
		[[ 1  2  3]
		 [ 4  5  6]
		 [ 7  8  9]
		 [10 11 12]]
		'''
		b = np.array([0,2,0,1]) # b.shape (4,) 单维
		print(b,b.shape)
		'''
		[0 2 0 1]
		'''
		print(a[np.arange(4),b]) # (0,0)1 (1,2)6 (2,0)7 (3,1) 11 #
		
		# 自增
		a[np.arange(4),b] +=10 # (0,0) (1,2) (2,0) (3,1) 全部在当前基础上 +10
		print(a)
		
		# bool 过滤
		a = np.array([[1,2],[3,4],[5,6]])
		bool_idx = (a>2) # 遍历矩阵元素，进行bool 判断，符合条件返回 True 否则返回 False
		print(bool_idx)
		'''
		[[False False]
        [ True  True]
        [ True  True]]
		'''
		
		print(a[a>2]) # 取出矩阵中 元素 >2 的元素，构成list 返回 [3 4 5 6]
		
		# 元素长度
		x = np.array([1,2],dtype=np.int32)
		print(x.dtype)  # int32
		
		x = np.array([1,2],dtype=np.int64)
		print(x.dtype)  # int64
		
		x = np.array([1,2],dtype=np.float32)
		print(x.dtype)  # float32
		
		x = np.array([111111111111111111111111111111111111111,111111111111111111111111111111111111111])
		print(x.dtype) # object 长度超限，自动适应object
		
		# 矩阵运算 + - * / sqrt
		x = np.array([[1,2],[3,4]],dtype=np.float64)
		y = np.array([[5,6],[7,8]],dtype=np.float64)
		
		print(x+y)
		print(np.add(x,y)) # 矩阵相加
		'''
		[[  6.   8.]
         [ 10.  12.]]
		'''
		
		print(x - y)
		print(np.subtract(x,y)) # 矩阵相减
		'''
		[[-4. -4.]
         [-4. -4.]]
		'''
		
		print(x * y)
		print(np.multiply(x,y)) # 矩阵相乘
		'''
		[[  5.  12.]
         [ 21.  32.]]
		'''
		
		print(x / y)
		print(np.divide(x,y))  # 矩阵相除
		'''
		[[ 0.2         0.33333333]
        [ 0.42857143  0.5       ]]
		'''
		
		print(np.sqrt(x)) # 矩阵每个元素进行开方
		'''
		[[ 1.          1.41421356]
         [ 1.73205081  2.        ]]
		'''
		
		# 集合 求 点积
		v = np.array([9,10])
		w = np.array([11,12])
		
		print(v.dot(w))
		print(np.dot(v,w)) # 点积，相同位置元素相乘，求和
		'''
		|9 |     |11|
		|  | dot |  |  =  9 *11 + 10*12
		|10|     |12|
		
		'''
		
		# 矩阵求点积
		x = np.array([[1,2],[3,4]]) # np 的行列 与代数行列相反
		y = np.array([[5,6],[7,8]])
		print(x)
		print(y)
		print(x.dot(y))
		print(np.dot(x,y))
		'''
		|1   3|       |5   7|   |(1,2)x(5,7)   (3,4)x(5,7)|   |5+14  15+28|   |19  43|
		|     |  dot  |     | = |                         | = |           | = |      |
		|2   4|       |6   8|   |(1,2)x(6,8)   (3,4)x(6,8)|   |6+16  18+32|   |22  50|
		
		'''
		print(x[0,1]) # 0列1行位置元素
		
		print(np.sum(x)) # 1+2+3+4
		print(np.sum(x,axis=0)) # 0轴 -> [4,6]
		print(np.sum(x,axis=1)) # 1轴 -> [3,7]
		
		
		# 转置 多维矩阵转置 行列切换，单维转置，不做人格改变
		a = np.array([[1,2],[3,4]])
		print(a)
		print(a.T)
		'''
		[[1 2][3 4]] -> [[1 3][2 4]]
		'''
		
		b = np.array([1,2,3])
		print(b)
		print(b.T)
		'''
		[1 2 3] -> [1 2 3]
		'''
		
		# broadcasting
		a = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
		b = np.array([1,0,1])
		v = np.empty_like(a) # 以a.shape 为基础创建空矩阵，矩阵行列式为0
		print(v)
		'''
		[[-8070450532247928832 -8070450532247928832                    7]
		 [     140389039587296                    0                    0]
		 [                   6                    0      140389039587296]
		 [     140389039587328                    0                    0]]
		'''
		# 填充
		for i in range(4):
			v[i,:] = a[i,:] + b
		
		print(v)
		'''
		[[ 2  2  4]
		 [ 5  5  7]
		 [ 8  8 10]
		 [11 11 13]]
		'''
		
		# copy
		a = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
		b = np.array([1,0,1])
		
		v = np.tile(b,(4,2)) # 将b重复拉出4列，每列重复2次
		print(v)
		'''
		[[1 0 1 1 0 1]
		 [1 0 1 1 0 1]
		 [1 0 1 1 0 1]
		 [1 0 1 1 0 1]]
		'''
		
		vv = np.tile(b,(4,1)) # 将b重复拉出4列，每列重复一次
		print(vv)
		'''
		[[1 0 1]
		 [1 0 1]
		 [1 0 1]
		 [1 0 1]]
		'''
		
		aa = a+vv
		print(aa)  # 矩阵求和
		'''
		[[ 2  2  4]
		 [ 5  5  7]
		 [ 8  8 10]
		 [11 11 13]]
		'''
		
		a = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
		b = np.array([1,0,1])
		c = a+b # a 的每一列 与 b 相加
		print(c)
		'''
		[[ 2  2  4]
		 [ 5  5  7]
		 [ 8  8 10]
		 [11 11 13]]
		'''
		
		# 矩阵运算
		v = np.array([1,2,3])
		w = np.array([4,5])
		
		print(np.reshape(v,(3,1))*w) # (3,) => (3,1), (3,1)*(2,) =>(3,2)
		'''
						  |1*4 2*4 3*4|
		[1,2,3] * [4,5] = |           |
		                  |1*5 2*5 3*5|
		
		'''
		x = np.array([[1,2,3],[4,5,6]])
		print(x + v)
		'''
		[[2 4 6]
        [5 7 9]]
		'''
		
		print((x.T + w).T)
		'''                              |5 6|
		[1,2,3] + |4| = |1+4 2+4 3+4|  = |6 7|
		          |5|   |1+5 2+5 3+5|.T  |7 8|
		'''
		
		print(x + np.reshape(w,(2,1)))
		
		'''
		[[ 5  6  7]
        [ 9 10 11]]
		'''
		
		print(x*2) # 倍增
		'''
		[[ 2  4  6]
        [ 8 10 12]]
		'''
		
		
		
		
		
		
		
		pass
	
	finally:
		os._exit(0)



