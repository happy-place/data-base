#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""

import os,traceback,re,sys
import calendar
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
import pytz
from pytz import timezone,utc

def test_timedelta():
	a = timedelta(days=2,hours=6)
	b = timedelta(hours=4.5)
	c = a+b
	print(c,c.days,c.seconds/3600.0) # (datetime.timedelta(2, 37800), 2, 10.5) c.seconds > 除去days 之外时间换算成秒
	print(c.total_seconds()/3600.0) # 58.5 = 48 + 10.5 全部小时数


def test_datetime():
	a = datetime(2012,9,23)
	print(a+timedelta(days=10)) # 2012-10-03 00:00:00
	
	b = datetime(2012,12,21)
	d = b - a # 89
	print(d.days)
	
	now = datetime.today()
	print(now+timedelta(minutes=10)) # 2018-07-21 14:08:32.445644
	
	a = datetime(2012, 3, 1)
	b = datetime(2012, 2, 28)
	c = a - b
	print(c,c.days) # (datetime.timedelta(2), 2)

def get_previous_byday(dayname,start_date=None):
	weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	if start_date is None:
		start_date = datetime.today()
	day_num = start_date.weekday()
	day_num_target = weekdays.index(dayname)
	days_ago = (7 + day_num - day_num_target) % 7
	if days_ago == 0:
		days_ago = 7
	target_date = start_date+timedelta(days=-days_ago)
	return target_date


def test_relativedelta():
	a = datetime(2012,9,23)
	print(a + relativedelta(months=+1)) # 2012-10-23 00:00:00
	b = datetime(2012,12,21)
	d = b - a # 时间间隔
	print(d) # 89 days, 0:00:00
	d = relativedelta(b,a)
	print(d,d.months,d.days) # (relativedelta(months=+2, days=+28), 2, 28) months，days 只展示各维度上数值

	print(get_previous_byday(dayname='Monday')) # 2018-07-16 14:51:56.687660
	print(get_previous_byday(dayname='Sunday')) # 2018-07-15 14:53:03.833601
	print(get_previous_byday(dayname='Sunday',start_date=(datetime.today()+timedelta(days=7)))) # 2018-07-22 14:54:11.951962
	print(get_previous_byday(dayname='Sunday',start_date=datetime(2018,12,12))) # 2018-12-09 00:00:00

	
def test_rrule():
	d = datetime.now()
	print(d,d.weekday()) # (datetime.datetime(2018, 7, 21, 14, 58, 22, 343862), 5) 周天索引从0开始
	
	print(d+relativedelta(weekday=FR)) # from dateutil.rrule import * 2018-07-27 14:58:22.343862 相对于d 下个周五日期
	print(d+relativedelta(weekday=FR(-1))) # 2018-07-20 14:58:22.343862 相对于d 上个周五日期


def get_month_range(start_date=None):
	'''
	获取整月起止节点
	:param start_date:
	:return:
	'''
	if start_date is None:
		start_date = date.today().replace(day=1) # 将日替换成月始
	else:
		start_date = start_date.replace(day=1)
	start_date_weekdays,days_in_month = calendar.monthrange(start_date.year,start_date.month)
	print("月始周天: {w},总共天数: {d}".format(w=start_date_weekdays,d=days_in_month)) # 月始周天: 6,总共天数: 30
	print(days_in_month)
	end_date = start_date + timedelta(days=days_in_month)
	return (start_date,end_date)


def date_range(start,end,step):
	'''
	以生成器方式按指定频率滑动时间
	
	:param start:
	:param end:
	:param step:
	:return:
	'''
	while start <= end:
		yield start
		start +=step

def get_diff(start,end,fmt):
	start_dt = datetime.strptime(start, fmt)
	end_dt = datetime.strptime(end, fmt)
	return end_dt - start_dt

def get_nice_format():
	dt = datetime(2017,1,12,21,45,30,11221)
	print(datetime.strftime(dt,'%A %B %d, %Y')) # Thursday January 12, 2017

def parse_dt(dt_str):
	# dt = datetime.strftime(dt_str,'%Y-%m-%d')
	dt = datetime(*(int(x)for x in dt_str.split('-'))) # 2018-01-23 00:00:00
	print(dt)

def get_local_dt():
	dt = datetime(2018,7,21,9,30,45,0)
	us_zone = timezone('US/Central')
	us_dt = us_zone.localize(dt)
	print(us_dt) # 2018-07-21 09:30:45-05:00  注：-05:00 表明us_dt 比dt 慢5个时区
	
	akt_dt = us_dt.astimezone(timezone('Asia/Kolkata')) # 2018-07-21 20:00:45+05:30
	print(akt_dt) #dt , us_dt , akt_dt 这三个时间是同步的

def get_normalize_dt():
	'''
	在 2013 年，美国标准夏令时时间开始于本地时间 3 月 13 日凌晨 2:00(在那时，时 间向前跳过一小时)
	
	:return:
	'''
	dt = datetime(2013,3,10,1,45,0,0)
	us_zone = timezone('US/Central')
	loc_dt = us_zone.localize(dt)
	normalize_dt = us_zone.normalize(loc_dt+timedelta(minutes=30)) # 1:45 + 30min + 1h > 03:15
	print(normalize_dt) # 2013-03-10 03:15:00-05:00
	
def test_utc():
	# local -> us -> utc -> +30m -> us 避免夏令时
	dt = datetime(2013,3,10,1,45,0,0)
	us_zone = timezone('US/Central')
	loc_dt = us_zone.localize(dt)
	print(loc_dt) # 2013-03-10 01:45:00-06:00
	utc_dt = loc_dt.astimezone(utc)
	print(utc_dt) # 2013-03-10 07:45:00+00:00
	
	print((utc_dt+timedelta(minutes=30)).astimezone(us_zone)) # 2013-03-10 03:15:00-05:00

def get_zone():
	print(pytz.country_timezones['IN']) # [u'Asia/Kolkata']
	print(pytz.country_timezones['CN']) # [u'Asia/Shanghai', u'Asia/Harbin', u'Asia/Chongqing', u'Asia/Urumqi', u'Asia/Kashgar']
	
	



if __name__=="__main__":
	try:
		# test_timedelta()
		# test_datetime()
		# test_relativedelta()
		# test_rrule()
		
		# 得到月始月末
		# first_day,last_day = get_month_range(datetime(2018,4,23)) # (datetime.datetime(2018, 4, 1, 0, 0), datetime.datetime(2018, 5, 1, 0, 0))
		#
		# print(get_month_range(datetime(2018,4,23)))
		# while first_day <last_day:
		# 	print(first_day.__format__('%Y-%m-%d'))
		# 	first_day += timedelta(days=1)
		#
		
		# for d in date_range(datetime(2018,1,9),datetime(2018,1,18),timedelta(hours=12)):
		# 	print(d)
		
		# print(get_diff('2018-01-03 12:23:45','2018-01-21 17:16:20','%Y-%m-%d %H:%M:%S')) # 18 days, 4:52:35
		
		# get_nice_format()
		
		# parse_dt('2018-01-23')
		
		# get_local_dt()
		
		# get_normalize_dt()
		
		# test_utc()
		
		get_zone()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)







