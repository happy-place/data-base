#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/6/25'
Info:
    http://pandas.pydata.org/pandas-docs/stable/10min.html
    
"""

import pandas as pd
import numpy as np
import sys,os,traceback

import matplotlib.pyplot as plt

if __name__=="__main__":
	try:
		# 构建集合序列
		s = pd.Series([1,3,5,np.nan,6,8])
		for row in s:
			print(row)
		'''
		1.0
		3.0
		5.0
		nan
		6.0
		8.0
		'''
		
		print(s) # 带序号输出
		'''
		0    1.0
		1    3.0
		2    5.0
		3    NaN
		4    6.0
		5    8.0
		dtype: float64
		'''
		
		# (DatetimeIndex(['2018-06-02', '2018-06-03', '2018-06-04'], dtype='datetime64[ns]', freq='D'), <class 'pandas.core.indexes.datetimes.DatetimeIndex'>)
		# 可自动识别 日期格式
		dates = pd.date_range('20180602',periods=3)
		print(dates,type(dates))
		dates = pd.date_range('2018/06/02',periods=3)
		print(dates,type(dates))
		dates = pd.date_range('2018-06-02',periods=3)
		print(dates,type(dates))
		
		# 创建Dataframe         3行4列随机数矩阵 以时间序列为索引 列名
		df = pd.DataFrame(np.random.randn(3,4),index=dates,columns=list('ABCD'))
		print(df)
		'''
		                   A         B         C         D
		2018-06-02  0.879063  0.737705  1.934593  1.031008
		2018-06-03  1.788736  0.763112  0.751652  0.517088
		2018-06-04 -0.372570 -0.342579  0.137800  0.831877
		'''
		
		# 逐列定义dataframe
		df2 = pd.DataFrame({'A':1.,
							'B':pd.Timestamp('20180601'),
							'C':pd.Series(1,index=list(range(4)),dtype='float32'),
							'D':np.array([3]*4,dtype='int32'),
							'E':pd.Categorical(["test","train","test","train"]),
							'F':'foo'})
		
		print(df2,df2.dtypes)
		'''
		     A          B    C  D      E    F
		0  1.0 2018-06-01  1.0  3   test  foo
		1  1.0 2018-06-01  1.0  3  train  foo
		2  1.0 2018-06-01  1.0  3   test  foo
		3  1.0 2018-06-01  1.0  3  train  foo
		
		A           float64  每列的数据类型
		B    datetime64[ns]
		C           float32
		D             int32
		E          category
		F            object
		'''
		
		# 查看前2行,后2行
		print(df.head(2),df2.tail(2))
		'''
			            A        B         C         D
		2018-06-02  0.623778  1.75443  0.537328  0.206595
		2018-06-03 -0.867567  0.86087 -0.377275  1.683616,
		
			A   B           C   D      E    F
		2  1.0 2018-06-01  1.0  3   test  foo
		3  1.0 2018-06-01  1.0  3  train  foo
		
		'''
		
		# 查看 行索引 和 列名
		print(df.index,df2.columns)
		'''
		DatetimeIndex(['2018-06-02', '2018-06-03', '2018-06-04'], dtype='datetime64[ns]', freq='D'),
		Index([u'A', u'B', u'C', u'D', u'E', u'F'], dtype='object'))
		'''
		
		# 忽略列名 和 索引，打印数值
		print(df.values)
		'''
		 [-0.7887315   0.94242523  0.28845648  0.27347016]
		 [-1.37341829  0.25644935 -0.51923451 -0.4858264 ]
		 [ 1.10156737  0.73568235  0.56576023 -0.59264947]
		'''
		
		# 每列数据当成序列进行基本统计描述
		print(df.describe())
		'''
		              A         B         C         D
		count  3.000000  3.000000  3.000000  3.000000
		mean  -0.353527  0.644852  0.111661 -0.268335
		std    1.293615  0.351892  0.563690  0.472247
		min   -1.373418  0.256449 -0.519235 -0.592649
		25%   -1.081075  0.496066 -0.115389 -0.539238
		50%   -0.788732  0.735682  0.288456 -0.485826
		75%    0.156418  0.839054  0.427108 -0.106178
		max    1.101567  0.942425  0.565760  0.273470
		'''
		
		# 行列转置
		print(df.T)
		'''
		   2018-06-02  2018-06-03  2018-06-04
		A   -0.652419   -0.829209    1.566238
		B    1.002829    0.633701   -0.323278
		C    1.347338    0.110144    0.106300
		D    0.494068   -0.522697    0.678159
		'''
		
		# 基于 y 轴(索引) 进行排序，降序输出
		print(df.sort_index(axis=0,ascending=False))
		'''
		                   A         B         C         D
		2018-06-04  0.255547 -1.209493  0.086225 -0.904646
		2018-06-03  0.268824 -2.102548  0.242114 -1.736373
		2018-06-02 -0.585154  1.439210  0.433746  1.023873
		'''
		
		# 基于 x 轴(列名) 进行排序，降序输出
		print(df.sort_index(axis=1,ascending=False))
		'''
		                   D         C         B         A
		2018-06-02  1.023873  0.433746  1.439210 -0.585154
		2018-06-03 -1.736373  0.242114 -2.102548  0.268824
		2018-06-04 -0.904646  0.086225 -1.209493  0.255547
		'''
		
		# 基于 第 4 列进行排序，升序输出
		print(df.sort_values(by='D',ascending=True))
		'''
		                   A         B         C         D
		2018-06-03 -1.329334 -0.070949  0.732712 -1.567207
		2018-06-02  0.448837 -0.757863 -0.240232 -0.739911
		2018-06-04 -0.340379  0.171098  0.660514  2.349389
		Freq: D, Name: A, dtype: float64
		'''
		
		# 取出指定列的序列
		print(df['A'])
		'''
		2018-06-02   -0.192238
		2018-06-03    2.157621
		2018-06-04   -0.314811
		Freq: D, Name: D, dtype: float64
		'''
		
		print(df['D'])
		'''
		2018-06-02   -1.323099
		2018-06-03   -0.180967
		2018-06-04   -0.630904
		Freq: D, Name: D, dtype: float64
		'''
		
		# 取第1，3 行
		print(df[1:3])
		'''
		                   A         B         C         D
		2018-06-03 -1.231567 -0.393768  0.318017 -1.104432
		2018-06-04  0.814158  1.313890  0.009524  0.741683
		'''
		
		# 提取指定范围内的记录
		print(df['2018-06-03':])
		'''
		                   A         B         C         D
		2018-06-03 -1.041590  0.459046 -0.288298 -0.542265
		2018-06-04 -0.164296 -0.552780  0.454403 -0.371269
		'''
		
		# 提取指定范围内的记录
		print(df[:"2018/06/03"])
		'''
		                   A         B         C         D
		2018-06-02  0.590981 -1.472029 -0.143457 -1.411623
		2018-06-03 -1.041590  0.459046 -0.288298 -0.542265
		'''
		
		# dates[1] 锁定索引 df.loc[index_val] 取指定索引所在的行
		print(df.loc[dates[1]])
		'''
		A    0.357734
		B   -1.580258
		C    0.031689
		D    0.599910
		Name: 2018-06-03 00:00:00, dtype: float6
		'''
		
		# 取指定列 的全部数据
		print(df.loc[:,['A','B']])
		'''
		                   A         B
		2018-06-02 -0.243493  0.370777
		2018-06-03 -1.330290  0.258503
		2018-06-04 -0.661972 -0.280612
		'''
		
		# 取指定列的固定行的数据
		print(df.loc[dates[1],['A','B']])
		'''
		A   -1.330290
		B    0.258503
		'''
		
		# 查指定行，指定列数据
		print(df.loc[dates[1],'A'])
		'''
		1.11529508646
		'''
		
		# 取 第0行数据
		print(df.iloc[0])
		'''
		A   -0.659377
		B   -0.360344
		C   -1.233967
		D   -0.554631
		'''
		
		# 取第[1,3) 行的第 [1,3) 列的数据 左闭右开，不会检测越界
		print(df)
		print(df.iloc[1:3,1:3])
		'''
							0         1         2         3
				            A         B         C         D
		0>> 2018-06-02 -0.186587 -0.512724  1.484470 -0.977484
							      ---------------------
		1>> 2018-06-03  0.289932 |-0.177223  0.043938 |-1.384691
		2>> 2018-06-04 -0.304986 |-0.687821  1.214720 | 0.857895
							      ---------------------
		
		                B         C
		2018-06-03 -0.177223  0.043938
		2018-06-04 -0.687821  1.214720
		'''
		
		# 取 第1，2 行对应 第 1，2列元素
		print(df.iloc[[1,2],[1,2]])
		'''
						   0         1         2         3
		                   A         B         C         D
		0>> 2018-06-02  1.156968  1.639000 -2.173309 -0.023107
		1>> 2018-06-03  2.347609 -0.720677  0.259880  1.202848
		2>> 2018-06-04  0.991807  0.014514 -0.758443  0.666414

		                   B         C
		2018-06-03 -0.720677  0.259880
		2018-06-04  0.014514 -0.758443
		'''
		
		# 取 [0,2) 行全部列元素
		print(df.iloc[0:2,:])
		'''
		                A         B         C         D
		2018-06-02  0.067523 -1.957399  1.655923 -0.080533
		2018-06-03  1.191417 -1.690492  0.927969 -0.026421
		'''
		
		# 取全部行,[1,3) 列元素
		print(df.iloc[:,1:3])
		
		# 取 坐标为 (1,2) 号元素
		print(df.iloc[1,2])
		'''
						   0         1         2         3
		                   A         B         C         D
		0>> 2018-06-02  0.969667  1.011982 -1.413178 -1.009500
		1>> 2018-06-03  1.198965  2.035735 -0.085357  1.605931
		2>> 2018-06-04 -1.332224 -2.486864  0.135822 -0.081157
		
		-0.0853574477099
		'''
		
		# 取 坐标为 (1,2) 号元素
		print(df.iat[1,2])
		'''
							0         1         2         3
		                    A         B         C         D
		0>> 2018-06-02 -0.500641 -1.205787  0.090146  2.620817
		1>> 2018-06-03  0.823671 -0.495762  1.551303 -2.073188
		2>> 2018-06-04  0.719998  0.186241 -0.315221  1.074823
		
		1.55130331899
		'''
		
		# 对 'D' 列进行重新赋值
		df.loc[:,'D'] = np.array([5] * len(df))
		print(df)
		'''
		                A         B         C  D
		2018-06-02 -1.288337  0.148548 -1.079238  5
		2018-06-03  0.854436 -0.445560 -0.330683  5
		2018-06-04 -1.919161  0.198471  0.183154  5
		'''
		
		# 深浅拷贝 默认 deep = True
		df3 = df.copy(deep=False)
		df4 = df.copy(deep=True)
		print(id(df),id(df3),id(df4))
		'''
		(4484474704, 4513050128, 4512907984)
		'''
		
		print(id(df.iat[1,1]),id(df3.iat[1,1]),id(df4.iat[1,1]))
		'''
		(4360111592, 4360111592, 4360111592)
		'''
		
		# 将大于0元素进行反转
		df3[df>0] = -df3
		print(df)
		print(df3)
		print(df4)
		'''
		                   A         B         C  D
		2018-06-02 -0.600809 -0.157217 -0.015304  5
		2018-06-03 -1.314965 -0.492321 -0.667259  5
		2018-06-04 -1.922268 -1.646287 -0.211133  5
		                   A         B         C  D
		2018-06-02 -0.600809 -0.157217 -0.015304 -5
		2018-06-03 -1.314965 -0.492321 -0.667259 -5
		2018-06-04 -1.922268 -1.646287 -0.211133 -5
		                   A         B         C  D
		2018-06-02 -0.600809 -0.157217  0.015304  5
		2018-06-03 -1.314965  0.492321 -0.667259  5
		2018-06-04  1.922268 -1.646287  0.211133  5
		
		'''
		
		# 重建索引：对 [0:3) 行元素添加新列 'E', 对[0:1]行，'E'列赋值 1.0 ,第2行'E'列取默认值'NaN'
		df5 = df.reindex(index=dates[0:3], columns=list(df.columns) + ['E'])
		df5.loc[dates[0]:dates[1],'E'] = 1.0
		print(df5)
		'''
		                A         B         C  D    E
		2018-06-02 -0.894034 -1.481198 -1.269124  5  1.0
		2018-06-03 -1.219157 -1.133296 -1.590058  5  1.0
		2018-06-04 -0.878932 -0.248505 -0.421544  5  NaN
		'''
		
		# 列方向扫描，一旦出现 Nan 删除整列
		df6 = df5.dropna(axis=1,how='any')
		print(df6)
		'''
                           A         B         C  D
		2018-06-02 -0.560570 -1.028436 -0.548013  5
		2018-06-03 -0.906676 -1.906432 -1.096828  5
		2018-06-04 -0.168472 -0.786563 -1.292570  5
		'''
		
		# 行方向扫描，一旦出现 Nan 删除整行
		df7 = df5.dropna(axis=0,how='any')
		print(df7)
		'''
		                   A         B         C  D    E
		2018-06-02 -0.560570 -1.028436 -0.548013  5  1.0
		2018-06-03 -0.906676 -1.906432 -1.096828  5  1.0
		'''
		
		# 填空
		df8 = df5.fillna(value=100.0)
		print(df8)
		'''
		                   A         B         C  D      E
		2018-06-02 -1.963754 -0.092817 -1.635404  5    1.0
		2018-06-03 -0.015473 -0.562273 -0.620076  5    1.0
		2018-06-04 -2.089162 -1.756256 -0.039724  5  100.0
		'''
		
		# 基于是否为空，计算 mask 矩阵
		df9 = df5.isnull()
		print(df9)
		'''
		                A      B      C      D      E
		2018-06-02  False  False  False  False  False
		2018-06-03  False  False  False  False  False
		2018-06-04  False  False  False  False   True
		
		'''
		
		# 按列计算均值,默认按列计算，等效于 df.mean(0)
		print(df.mean())
		'''
		A   -0.729484
		B   -0.437087
		C   -0.743955
		D    5.000000
		dtype: float64
		'''
		
		print(df.mean(1))
		'''
		2018-06-02    1.003401
		2018-06-03    0.698900
		2018-06-04    0.907924
		'''
		
		# 构建 Series
		dates = pd.date_range('20180601',periods=6)
		s = pd.Series([1,3,5,np.nan,6,8], index=dates)
		print(s)
		'''
		2018-06-01    1.0
		2018-06-02    3.0
		2018-06-03    5.0
		2018-06-04    NaN
		2018-06-05    6.0
		2018-06-06    8.0
		Freq: D, dtype: float64
		'''
		
		# 下推两行
		s =	s.shift(2)
		print(s)
		'''
		2018-06-01    NaN
		2018-06-02    NaN
		2018-06-03    1.0
		2018-06-04    3.0
		2018-06-05    5.0
		2018-06-06    NaN
		Freq: D, dtype: float64
		'''
		
		# 6行4列，以 dates 为索引，ABCD 为列名 构建 DF
		df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
		# substract df - s
		print(df)
		
		dfs = df.sub(s, axis='index')
		print(dfs)
		'''
		                A         B         C         D
		2018-06-01 -0.792830 -0.235912  0.888408 -0.215030
		2018-06-02  0.415691  0.096511  0.569419  0.304519
		2018-06-03  0.160147 -0.366209  0.620800  0.526143
		2018-06-04 -0.427479  0.675759  1.670183 -1.209437   -
		2018-06-05 -1.736107  1.136996 -0.507994 -0.071502
		2018-06-06 -0.516211  1.463763 -0.483547  0.389332
		
		2018-06-01    NaN
		2018-06-02    NaN
		2018-06-03    1.0
		2018-06-04    3.0     =
		2018-06-05    5.0
		2018-06-06    NaN
		
		                 A         B         C         D
		2018-06-01       NaN       NaN       NaN       NaN
		2018-06-02       NaN       NaN       NaN       NaN
		2018-06-03 -0.839853 -1.366209 -0.379200 -0.473857
		2018-06-04 -3.427479 -2.324241 -1.329817 -4.209437
		2018-06-05 -6.736107 -3.863004 -5.507994 -5.071502
		2018-06-06       NaN       NaN       NaN       NaN
		
		'''
		
		# 沿 axis = 0 y轴 累加,默认沿纵轴(axis=0)计算
		dfc0 = df.apply(np.cumsum,axis=0)
		dfc1 = df.apply(np.cumsum,axis=1)
		print("df.apply(np.cumsum,axis=0)")
		print(dfc0)
		print(dfc1)
		'''
		                   A         B         C         D
		----------------------------------------------------> 1
		|2018-06-01 -1.214361 -0.544017 -0.899966  0.479818
		|2018-06-02  1.224434  0.078369  0.269104  0.248419
		|2018-06-03  0.862227 -1.074286 -0.539268 -0.343966
		|2018-06-04 -0.925328 -0.347535  1.347204 -0.954560
		|2018-06-05 -1.806960  0.692161  0.268760 -0.320073
		|2018-06-06  1.654026 -1.313658  1.072770 -0.012696
		|
		↓
		0
	
		按 axis = 0 纵轴汇总
		                   A         B         C         D
		2018-06-01 -1.214361 -0.544017 -0.899966  0.479818
		2018-06-02  0.010073 -0.465648 -0.630862  0.728237
		2018-06-03  0.872300 -1.539934 -1.170130  0.384271
		2018-06-04 -0.053028 -1.887469  0.177074 -0.570289
		2018-06-05 -1.859988 -1.195307  0.445834 -0.890362
		2018-06-06 -0.205961 -2.508966  1.518604 -0.903058
		
		按 axis = 1 横轴汇总
		                   A         B         C         D
		2018-06-01 -1.214361 -1.758377 -2.658344 -2.178526
		2018-06-02  1.224434  1.302803  1.571907  1.820326
		2018-06-03  0.862227 -0.212059 -0.751327 -1.095293
		2018-06-04 -0.925328 -1.272863  0.074341 -0.880219
		2018-06-05 -1.806960 -1.114798 -0.846039 -1.166112
		2018-06-06  1.654026  0.340368  1.413138  1.400441
		
		'''
	
		dfa0 = df.apply(lambda x:x.max() - x.min(),axis=0)
		dfa1 = df.apply(lambda x:x.max() - x.min(),axis=1)
		print("------")
		dfa1 = df.apply(lambda x:x.sum(),axis=0)
		print(dfa1)
		print("------")
		print(" df.apply(lambda x:x.max() - x.min(),axis=0)")
		print(dfa0)
		print(dfa1)
		'''
		                   A         B         C         D
		2018-06-01 -1.214361 -0.544017 -0.899966  0.479818
		2018-06-02  1.224434  0.078369  0.269104  0.248419
		2018-06-03  0.862227 -1.074286 -0.539268 -0.343966
		2018-06-04 -0.925328 -0.347535  1.347204 -0.954560
		2018-06-05 -1.806960  0.692161  0.268760 -0.320073
		2018-06-06  1.654026 -1.313658  1.072770 -0.012696
		
		按 axis = 0 纵轴计算
		A    3.460986
		B    2.005820
		C    2.247171
		D    1.434378
		
		按 axis = 1 横轴计算
		2018-06-01    1.694179
		2018-06-02    1.146066
		2018-06-03    1.936512
		2018-06-04    2.301764
		2018-06-05    2.499121
		2018-06-06    2.967685
		'''
		
		# 创建Series 序列，去 [0,7] 间的随机整数填充
		s = pd.Series(np.random.randint(0,7,size=10))
		print(s)
		'''
		0    2
		1    3
		2    1
		3    0
		4    1
		5    5
		6    6
		7    6
		8    6
		9    6
		'''
		
		# wordcount 统计
		print(s.value_counts(ascending=True))
		'''
		0    1
		2    1
		3    1
		5    1
		1    2
		6    4  << 4 个 6
		'''
	
		# 对全部字符串进行转小写处理
		s = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])
		sl = s.str.lower()
		print(sl)
		'''
		0       a
		1       b
		2       c
		3    aaba
		4    baca
		5     NaN
		6    caba
		7     dog
		8     cat
		'''
		
		# Merge
		# 创建 10行4列 DF
		df = pd.DataFrame(np.random.randn(10, 4))
		# 按 [0,3),[3,7),[7,end] 行进行拆分
		pieces = [df[:3],df[3:7],df[7:]]
		print(pieces[0])
		print(pieces[1])
		print(pieces[2])
		'''
	              0         1         2         3
		0 -0.244026 -0.548166 -1.190074 -0.127160
		1 -1.079754 -0.211218  0.373533  0.190856
		2  1.386175 -0.266816 -1.264290  1.725484
		          0         1         2         3
		3  0.233429  1.406712  0.226452 -0.432027
		4 -0.635829 -0.672521 -0.011322 -0.767775
		5 -1.197380 -1.114208 -0.706888  0.454968
		6 -0.246094 -0.218817  0.010268 -0.178705
		          0         1         2         3
		7  0.321441  1.641240 -0.080133 -0.354089
		8  0.604506  1.501262  1.040242  1.703835
		9  0.256772 -0.825002 -0.663802  0.219656
		'''
		
		# 同列合并，自栋参照行号排序
		print(pd.concat(pieces))
		'''
		          0         1         2         3
		0 -0.244026 -0.548166 -1.190074 -0.127160
		1 -1.079754 -0.211218  0.373533  0.190856
		2  1.386175 -0.266816 -1.264290  1.725484
		3  0.233429  1.406712  0.226452 -0.432027
		4 -0.635829 -0.672521 -0.011322 -0.767775
		5 -1.197380 -1.114208 -0.706888  0.454968
		6 -0.246094 -0.218817  0.010268 -0.178705
		7  0.321441  1.641240 -0.080133 -0.354089
		8  0.604506  1.501262  1.040242  1.703835
		9  0.256772 -0.825002 -0.663802  0.219656
		'''
		
		# 存在多匹配项时，各匹配项依次合并
		left = pd.DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
		right = pd.DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})
		
		mergeV = pd.merge(left,right,on='key')
		
		print(left)
		print(right)
		print(mergeV)
		'''
		   key  lval
		0  foo     1
		1  foo     2
		
		   key  rval
		0  foo     4
		1  foo     5
		
		   key  lval  rval
		0  foo     1     4
		1  foo     1     5
		2  foo     2     4
		3  foo     2     5
		'''
		
		# 单个匹配项之间合并即可
		left = pd.DataFrame({'key': ['foo1', 'foo2'], 'lval': [1, 2]})
		right = pd.DataFrame({'key': ['foo1', 'foo2'], 'rval': [4, 5]})
		
		mergeV = pd.merge(left,right,on='key')
		
		print(left)
		print(right)
		print(mergeV)
		'''
		    key  lval
		0  foo1     1
		1  foo2     2
		
		    key  rval
		0  foo1     4
		1  foo2     5
		
		    key  lval  rval
		0  foo1     1     4
		1  foo2     2     5
		
		'''
		
		# Append 追加
		# 8行4列，使用 0~1 之间随机数填充，列名为 ABCD
		df = pd.DataFrame(np.random.randn(8, 4), columns=['A','B','C','D'])
		print(df)
		'''
		          A         B         C         D
		0  0.196433 -1.812039 -0.331284  0.486081
		1 -0.905287  0.643512  0.082922 -0.197414
		2  1.649922 -0.900071  0.736035  0.488609
		3 -0.646371  1.510340  0.940653  0.448209  <<<
		4  0.571561  0.624087  1.066437 -0.863908
		5  0.085210  0.747587 -0.464181  0.535867
		6  1.256957 -0.367725 -0.312750 -0.907821
		7 -0.783526  0.300569  1.264514 -0.219418
		'''
		
		# 取 索引 index = 3 （从0开始，即第4行）的行
		s = df.iloc[3]
		dfd = df.append(s, ignore_index=True)
		print(dfd)
		'''
	              A         B         C         D
		0  0.196433 -1.812039 -0.331284  0.486081
		1 -0.905287  0.643512  0.082922 -0.197414
		2  1.649922 -0.900071  0.736035  0.488609
		3 -0.646371  1.510340  0.940653  0.448209
		4  0.571561  0.624087  1.066437 -0.863908
		5  0.085210  0.747587 -0.464181  0.535867
		6  1.256957 -0.367725 -0.312750 -0.907821
		7 -0.783526  0.300569  1.264514 -0.219418
		8 -0.646371  1.510340  0.940653  0.448209
		'''
		
		# 枚举各列创建DF
		df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
		                          'foo', 'bar', 'foo', 'foo'],
		                   'B' : ['one', 'one', 'two', 'three',
		                          'two', 'two', 'one', 'three'],
		                   'C' : np.random.randn(8),
		                   'D' : np.random.randn(8)
		                   })
		
		print(df)
		'''
		     A      B         C         D
		0  foo    one -1.308052  1.255266
		1  bar    one  1.827670 -0.162399
		2  foo    two -1.152499  0.354347
		3  bar  three -0.024736 -0.833156
		4  foo    two -1.409466 -0.619587
		5  bar    two  0.596132 -0.530647
		6  foo    one  0.236373  0.589717
		7  foo  three -2.303024  1.187029
		'''
		
		# 参照A 将所有数值没写进行汇总
		dfgs = df.groupby('A').sum()
		print(dfgs)
		'''
		A
		bar  2.399067 -1.526203
		foo -5.936668  2.766773
		'''
		
		# 取最值
		dfgs = df.groupby('A').max()
		print(dfgs)
		'''
		A      B         C         D
		bar  two  1.582268  1.728768
		foo  two  0.120770  1.266922
		'''
		
		# 二级分组 汇总
		dfgs = df.groupby(['A','B']).sum()
		print(dfgs)
		'''
		A   B
		bar one    1.102602  2.007118
		    three -0.616889 -1.801638
		    two   -2.015196  0.271078
		foo one    0.848364 -0.073521
		    three  0.173783  1.728719
		    two   -2.296201  1.173208
		'''

		# 多级索引
		tuples = list(zip(*[['bar', 'bar', 'baz', 'baz','foo', 'foo', 'qux', 'qux'], # 一级索引
		                    ['one', 'two', 'one', 'two','one', 'two', 'one', 'two']])) # 二级索引
		index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second']) # 创建多级索引
		df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=['A', 'B']) # 组合DataFrame
		
		df2 = df[:4]
		print(df)
		print(df2)
		'''
	                     A         B
		first second
		bar   one     0.991898 -0.642965
		      two     2.061375  0.349216
		baz   one    -1.371576 -0.344453
		      two    -0.586903 -0.434475
		foo   one     0.911436 -0.016167
		      two     1.501402  1.509269
		qux   one    -0.564117 -0.219454
		      two     0.947133 -0.470867
		      
		                     A         B
		first second
		bar   one     0.991898 -0.642965
		      two     2.061375  0.349216
		baz   one    -1.371576 -0.344453
		      two    -0.586903 -0.434475
		'''
		
		# 折叠
		df2_stacked = df2.stack()
		print(df2_stacked)
		'''
		first  second
		bar    one     A    0.991898
		               B   -0.642965
		       two     A    2.061375
		               B    0.349216
		baz    one     A   -1.371576
		               B   -0.344453
		       two     A   -0.586903
		               B   -0.434475
		'''
		
		# 解封 默认从最小级别开始 等效于 （0，1，2）三个级别轮转
		df2_unstacked = df2_stacked.unstack(2) # 沿最小粒度解封
		df1_unstacked = df2_stacked.unstack(1) # 沿 second 解封
		df0_unstacked = df2_stacked.unstack(0) # 沿 first 解封
		
		print(df2_unstacked)
		print(df1_unstacked)
		print(df0_unstacked)
		
		'''
	                     A         B
		first second
		bar   one     0.663427  0.184888
		      two     1.834347  0.250066
		baz   one    -1.971239 -0.589056
		      two    -0.231932 -1.288225
		      
		second→        one       two
		first↓
		bar   A  0.663427  1.834347
		      B  0.184888  0.250066
		baz   A -1.971239 -0.231932
		      B -0.589056 -1.288225
		      
		first          bar       baz
		second
		one    A  0.663427 -1.971239
		       B  0.184888 -0.589056
		two    A  1.834347 -0.231932
		       B  0.250066 -1.288225
		'''
		
		# Pivot Tables
		df = pd.DataFrame({'A' : ['one', 'one', 'two', 'three'] * 3,
		                   'B' : ['A', 'B', 'C'] * 4,
		                   'C' : ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2,
		                   'D' : np.random.randn(12),
		                   'E' : np.random.randn(12)})
		
		print(df)
		'''
		        A  B    C         D         E
		0     one  A  foo -1.776400  0.462332
		1     one  B  foo -0.869513 -0.284266
		2     two  C  foo -0.779028 -0.340096
		3   three  A  bar  0.249722 -0.630336
		4     one  B  bar  0.597383  0.276210
		5     one  C  bar -1.139131 -0.212623
		6     two  A  foo -0.225203 -1.896804
		7   three  B  foo  1.429117  0.397235
		8     one  C  foo -0.599256  0.890031
		9     one  A  bar  1.287133 -0.336844
		10    two  B  bar -0.352514  0.762982
		11  three  C  bar  0.779438 -0.404281
		'''
		
		# 以 AB为二级索引，D列为数据源，快速创建pivot_table
		df_pivot = pd.pivot_table(df, values='D', index=['A', 'B'], columns=['C'])
		print(df_pivot)
		'''
		C→           bar       foo
		A ↓   B↓
 		one   A  1.287133 -1.776400
		      B  0.597383 -0.869513
		      C -1.139131 -0.599256
		three A  0.249722       NaN
		      B       NaN  1.429117
		      C  0.779438       NaN
		two   A       NaN -0.225203
		      B -0.352514       NaN
		      C       NaN -0.779028
		'''
		
		rng = pd.date_range('1/1/2012', periods=100, freq='S') # 100 个元素，Seconds 级别序列,T 小时，D 天,M 月
		print(rng)
		'''
		DatetimeIndex(['2012-01-01 00:00:00', '2012-01-01 00:00:01',
               '2012-01-01 00:00:02', '2012-01-01 00:00:03',
               '2012-01-01 00:00:04', '2012-01-01 00:00:05',
               '2012-01-01 00:00:06', '2012-01-01 00:00:07',
               。。。。。。。。。。
		'''
		
		# 以时间为索引，取[0.500)内随机数 构建新序列
		ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
		print(ts)
		'''
		2012-01-01 00:00:00    216
		2012-01-01 00:00:01     14
		2012-01-01 00:00:02    493
		2012-01-01 00:00:03    331
		。。。。。。。。。
		'''
		# 重新以5min 频率采样汇总
		df_res = ts.resample('5Min')
		
		res = df_res.sum()
		print(df_res)
		print(res)
		
		# 时区转换，以天为间隔，取5天数据
		rng = pd.date_range('3/6/2012 00:00', periods=5, freq='D')
		# 关联随机是
		ts = pd.Series(np.random.randn(len(rng)), rng)
		print(ts)
		'''
		2012-03-06   -1.586120
		2012-03-07    0.763231
		2012-03-08    2.560824
		2012-03-09    0.535908
		2012-03-10    0.905008
		'''
		
		ts_utc = ts.tz_localize('UTC') # 调整为 UTC 时间
		print(ts_utc)
		'''
		2012-03-06 00:00:00+00:00    0.921673
		2012-03-07 00:00:00+00:00   -1.663133
		2012-03-08 00:00:00+00:00   -2.565105
		2012-03-09 00:00:00+00:00   -0.189263
		2012-03-10 00:00:00+00:00   -0.877948
		'''
		
		# 时间回溯了5h
		df_es = ts_utc.tz_convert('US/Eastern')
		print(df_es)
		'''
		2012-03-05 19:00:00-05:00    0.921673
		2012-03-06 19:00:00-05:00   -1.663133
		2012-03-07 19:00:00-05:00   -2.565105
		2012-03-08 19:00:00-05:00   -0.189263
		2012-03-09 19:00:00-05:00   -0.877948
		'''
		
		ts = pd.Series(np.random.randn(len(rng)), index=rng)
		print(ts)
		'''
		2012-03-06    2.194906
		2012-03-07   -0.535518
		2012-03-08    2.370312
		2012-03-09    0.285044
		2012-03-10    0.075925
		'''
		
		ps = ts.to_period(freq='D')
		print(ps)
		'''
		2012-03-06    2.194906
		2012-03-07   -0.535518
		2012-03-08    2.370312
		2012-03-09    0.285044
		2012-03-10    0.075925
		'''
		
		ps = ts.to_period(freq='M')
		print(ps)
		'''
		2012-03    2.194906
		2012-03   -0.535518
		2012-03    2.370312
		2012-03    0.285044
		2012-03    0.075925
		'''

		df_ts = ps.to_timestamp(how='end')
		print(df_ts)
		'''
		2012-03-31    2.194906
		2012-03-31   -0.535518
		2012-03-31    2.370312
		2012-03-31    0.285044
		2012-03-31    0.075925
		'''
	
		prng = pd.period_range('1990Q1', '2000Q4', freq='Q-NOV')
		print(prng)
		'''
		PeriodIndex(['1990Q1', '1990Q2', '1990Q3', '1990Q4', '1991Q1', '1991Q2',
             '1991Q3', '1991Q4', '1992Q1', '1992Q2', '1992Q3', '1992Q4',
             '1993Q1', '1993Q2', '1993Q3', '1993Q4', '1994Q1', '1994Q2',
             '1994Q3', '1994Q4', '1995Q1', '1995Q2', '1995Q3', '1995Q4',
             '1996Q1', '1996Q2', '1996Q3', '1996Q4', '1997Q1', '1997Q2',
             '1997Q3', '1997Q4', '1998Q1', '1998Q2', '1998Q3', '1998Q4',
             '1999Q1', '1999Q2', '1999Q3', '1999Q4', '2000Q1', '2000Q2',
             '2000Q3', '2000Q4'],
            dtype='period[Q-NOV]', freq='Q-NOV')
		'''
		
		ts = pd.Series(np.random.randn(len(prng)), prng)
		print(ts)
		'''
		1990Q1    0.013688
		1990Q2    1.367023
		1990Q3    0.335224
		1990Q4   -0.221647
		1991Q1    0.789581
		1991Q2    1.478848
		1991Q3    1.581727
		..........
		'''
		
		ts.index = (prng.asfreq('M', 'e') + 1).asfreq('H', 's') + 9
		print(ts.head())
		'''
		1990-03-01 09:00    0.013688
		1990-06-01 09:00    1.367023
		1990-09-01 09:00    0.335224
		1990-12-01 09:00   -0.221647
		1991-03-01 09:00    0.789581
		'''
		
		# 创建DF
		df = pd.DataFrame({"id":[1,2,3,4,5,6], "raw_grade":['a', 'b', 'b', 'a', 'a', 'e']})
		print(df)
		'''
		   id raw_grade
		0   1         a
		1   2         b
		2   3         b
		3   4         a
		4   5         a
		5   6         e
		'''
		
		# 添加新列
		df["grade"] = df["raw_grade"].astype("category")
		print(df)
		'''
		   id raw_grade grade
		0   1         a     a
		1   2         b     b
		2   3         b     b
		3   4         a     a
		4   5         a     a
		5   6         e     e
		'''
		
		# 自动 按 原有 a，b，e 三个类型替换 成为 ["very good", "good", "very bad"]
		df["grade"].cat.categories = ["very good", "good", "very bad"]
		print(df)
		'''
		   id raw_grade      grade
		0   1         a  very good
		1   2         b       good
		2   3         b       good
		3   4         a  very good
		4   5         a  very good
		5   6         e   very bad
		
		'''
		
		df["grade"] = df["grade"].cat.set_categories(["very bad", "bad", "medium", "good", "very good"])
		print(df["grade"])
		'''
		0    very good
		1         good
		2         good
		3    very good
		4    very good
		5     very bad
		Name: grade, dtype: category
		Categories (5, object): [very bad, bad, medium, good, very good]
		'''
		
		print(df.sort_values(by="grade"))
		'''
		   id raw_grade      grade
		5   6         e   very bad
		1   2         b       good
		2   3         b       good
		0   1         a  very good
		3   4         a  very good
		4   5         a  very good
		'''
		
		
		print(df.groupby("grade").size())
		'''
		grade
		very bad     1
		bad          0
		medium       0
		good         2
		very good    3
		'''
		
		# 绘图 anconda 中出图
		ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
		ts = ts.cumsum()

		ts.plot()
		
		df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index,columns=['A', 'B', 'C', 'D'])
	
		df = df.cumsum()
	
		plt.figure(); df.plot(); plt.legend(loc='best')
	
		# input output
		# 保存为 ',' 分割
		ts.to_csv('/Users/huhao/software/idea_proj/data-base/api-test/pandas-test/data/foo.csv')
		# 读取
		df = pd.read_csv('/Users/huhao/software/idea_proj/data-base/api-test/pandas-test/data/foo.csv')
		print(df)
		'''
		     2000-01-01  1.67181529544
		0    2000-01-02       3.569296
		1    2000-01-03       3.387349
		2    2000-01-04       3.914845
		'''
		
		# HDF5 层次化数据集，适合存储大批量数据。方便检索
		df.to_hdf('/Users/huhao/software/idea_proj/data-base/api-test/pandas-test/data/foo.h5','df')
		hdf = pd.read_hdf('/Users/huhao/software/idea_proj/data-base/api-test/pandas-test/data/foo.h5','df')
		print(hdf)
		'''
				[999 rows x 2 columns]
		     2000-01-01  -0.0208365315593
		0    2000-01-02         -1.500612
		1    2000-01-03         -1.700888
		2    2000-01-04         -1.455175
		3    2000-01-05          0.039492
		'''
		
		df.to_excel('/Users/huhao/software/idea_proj/data-base/api-test/pandas-test/data/foo.xlsx', sheet_name='Sheet1')
		excel = pd.read_excel('/Users/huhao/software/idea_proj/data-base/api-test/pandas-test/data/foo.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
		print(excel)
		'''
		[999 rows x 2 columns]
		     2000-01-01  -1.27414048806
		0    2000-01-02       -1.711235
		1    2000-01-03       -0.100039
		2    2000-01-04        0.112599
		'''
		
		if pd.Series([False, True, False]):
			print("I was true")

	except:
		traceback.print_exc()
	
	finally:
		# sys.exit(0) # ipython 子进程还在
		os._exit(0) # 子进程退出





