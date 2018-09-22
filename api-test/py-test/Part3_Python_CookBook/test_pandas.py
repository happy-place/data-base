#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/27'
Info:
        
"""
import os,traceback
import pandas

def test_read():
	rats = pandas.read_csv('rats.csv',skipfooter=1) #skipfooter 到达行末标识后停止扫描
	# print(rats)
	
	# print(rats['Current Activity'])
	print(rats['Current Activity'].unique()) # 去重 ['Dispatch Crew' nan 'Request Sanitation Inspector' 'Inspect for Violation' 'FVI - Outcome']
	
	crew_dispatched = rats[rats['Current Activity'] == 'Request Sanitation Inspector']
	# print(len(crew_dispatched)) # 438
	# print(crew_dispatched['ZIP Code'])
	# print(crew_dispatched['ZIP Code'].value_counts()) # 相同值出现频次统计
	'''
	60647.0    41
	60625.0    35
	60651.0    25
	60618.0    24
	60657.0    19
	60641.0    16
	'''
	dates = crew_dispatched.groupby('Completion Date') # 基于Completion Date字段进行聚合
	
	# print(dates)
	# for k in dates:
	# 	print(k)
	'''
	[2 rows x 20 columns])
	('12/14/2011',       Creation Date                   ...                                                    Location
	78053    12/08/2011                   ...                     (41.80989439766831, -87.69547755825619)
	78055    12/08/2011                   ...                     (41.98785867829078, -87.74831825212424)
	78322    12/11/2011                   ...                     (41.75877041956438, -87.68176308183484)
	78461    12/12/2011                   ...                     (41.703775508395765, -87.6060459118975)
	[4 rows x 20 columns])
	'''
	
	date_counts = dates.size()
	# print(date_counts)
	'''
	11/23/2011     1
	12/12/2011     2
	12/14/2011     4
	'''
	
	# print(date_counts[0:10]) # 取前10行
	'''
	Completion Date
	01/03/2012    2
	01/12/2012    1
	01/20/2012    1
	02/01/2012    2
	02/06/2013    1
	'''
	# print(date_counts.sort_index()) # 基于 index 即 Completion Date 列进行排序
	
	print(date_counts.sort_values()) # 基于 value 即 统计数列进行排序
	'''
	08/30/2013     1
              ..
	10/11/2011     4
	04/16/2013     4
	12/14/2011     4
	09/27/2011     4
	08/02/2011     5
	07/12/2011     5
	05/26/2011     5
	'''
	
	# date_counts[-10:]
	#
	





if __name__=="__main__":
	try:
		
		test_read()
		
		
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)







