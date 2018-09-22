#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/6/27'
Info:

"""
import pandas as pd
import traceback,os

if __name__=="__main__":
	
	try:
		df = pd.read_csv("/Users/huhao/software/idea_proj/data-base/api-test/pandas-test/data/1.csv").fillna('-')
		'''
		orders,uid,name,country,r_level,up_log,charge30,his30axcharge,up_down,last_active_dt,warn,watch_len,watch_num,broadcast_num,watch_top3,reward_top3
		'''
		# tf = df['orders','uid','name']
		print(df[['orders','uid','name','country','r_level','up_log','charge30','his30maxcharge','up_down','last_active_dt','warn','watch_len','watch_num','broadcast_num','watch_top3','reward_top3']])
		df.to_csv('/Users/huhao/software/idea_proj/data-base/api-test/pandas-test/data/2.csv',header=False,index=False)
		
	except:
		traceback.print_exc()
			
	finally:
		os._exit(0)
		
	
	

