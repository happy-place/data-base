#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os,traceback,json
from collections import OrderedDict
'''
 OrderedDict 维持的是数据插入的顺序，底层通过双向链表实现，对插入顺序的维护。插入删除性能开销 和 存储开销比普通 dict 大很多
'''


def test_orderedDict():
	d = OrderedDict()
	d['foo'] = 5
	d['bar'] = 2
	d['spam'] = 3
	d['grok'] = 4
	
	for k in d:
		print(k,d[k])
	'''
	foo 5
	bar 2
	spam 3
	grok 4
	'''

def mk_orderedJson():
	d = OrderedDict()
	d['foo'] = 5
	d['bar'] = 2
	d['spam'] = 3
	d['grok'] = 4
	j = json.dumps(d)
	print(j) # {"foo": 5, "bar": 2, "spam": 3, "grok": 4}


if __name__=="__main__":
	try:
		test_orderedDict()
		
		mk_orderedJson()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)

