#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,json,pickle
from pprint import pprint
from collections import OrderedDict
from test.pickletester import metaclass

'''
JSON(JavaScript Object Notation)
'''

def test_json():
	data = {'name':'ACME','shares':100,'price':435.2}
	jsons_str = json.dumps(data) # dict 对象 -> str
	print(type(jsons_str),jsons_str) # <class 'str'> {"name": "ACME", "shares": 100, "price": 435.2}
	
	data2 = json.loads(jsons_str) # str -> dict对象
	print(data2) # {'name': 'ACME', 'shares': 100, 'price': 435.2}
	
	with open('json.txt','wt') as f: # dict 对象 -> file
		json.dump(data,f)
	
	with open('json.txt','rt') as f: # file -> dict 对象
		data3 = json.load(f)
		print(type(data3),data3) # <class 'dict'> {'name': 'ACME', 'shares': 100, 'price': 435.2}
	

def test_different():
	data = {'a':True,'b':'Hello','c':None}
	data_str = json.dumps(data)
	print(data_str) # {"a": true, "b": "Hello", "c": null}
	
	data2 = json.loads(data_str)
	print(data2) # {'a': True, 'b': 'Hello', 'c': None}
	
	'''
	{"a": true, "b": "Hello", "c": null}
	
	json 与 python 中的dict 几乎完全一致，支持类型有int,float,bool,str,None ,序列化过程 None -> null,True -> true,False -> false
	反序列会过程执行相应的逆操作
	'''

def test_pprint():
	data = {'completed_in': 0.074,
	        'max_id': 264043230692245504,
	        'max_id_str': '264043230692245504',
	        'next_page': '?page=2&max_id=264043230692245504&q=python&rpp=5',
	        'page': 1,
	        'query': 'python',
	        'refresh_url': '?since_id=264043230692245504&q=python',
	        'results': [{'created_at': 'Thu, 01 Nov 2012 16:36:26 +0000',
	                     'from_user': "tom"
	                     },
	                    {'created_at': 'Thu, 01 Nov 2012 16:36:14 +0000',
	                     'from_user': "jack"
	                     },
	                    {'created_at': 'Thu, 01 Nov 2012 16:36:13 +0000',
	                     'from_user': "lily"
	                     },
	                    {'created_at': 'Thu, 01 Nov 2012 16:36:07 +0000',
	                     'from_user': 'lucy'
	                     },
	                    {'created_at': 'Thu, 01 Nov 2012 16:36:04 +0000',
	                     'from_user': 'haha'
	                     }],
	        'results_per_page': 5,
	        'since_id': 0,
	        'since_id_str': '0'}

	pprint(data) # 分层级美化打印输出，基于key按字母顺序排序


def convert_2_ordereddict():
	datas = ['{"q": 1, "r": 4, "w": 3, "e": 2}','{"q": 0, "r": 3, "e": 6, "w": 2}','{"q": 4, "r": 4, "e": 2, "w": 2}']
	
	datas1 = (json.loads(data) for data in datas)
	print(list(datas1)[0])
	# OrderedDict 可以维持原Json key 顺序
	datas2 = (json.loads(data,object_pairs_hook=OrderedDict) for data in datas)
	print(list(datas2)[0])


class JSONObject:
	def __init__(self,d):
		self.__dict__ = d # 此处d 为传入的json.items, __dict__ 为属性字典
	
	def serialize(obj):
		# 自定义类序列化函数，封装元数据到字典，用户 json.dumps 时保存属性信息
		meta_dic = { '__classname__' : type(obj).__name__ }
		meta_dic.update(vars(obj)) # 直接从栈帧获取属性
		return meta_dic
	
	def unserialize(d):
		# 自定义类反序列化函数，从输入源，提取类名，然后通过 eval函数还原为自定义对象
		clsname = d.pop('__classname__', None)
		if clsname:
			obj = eval('{clsname}({d})'.format(clsname=clsname,d = d)) # Make instance without calling __init__
			return obj
		else:
			return d


def convert_2_pythondict():
	data = '{"name": "ACME", "shares": 50, "price": 490.1}'
	
	data = json.loads(data,object_hook=JSONObject) # 反序列化，并将items 集合封装到自定义的 python对象JSONObject
	print(data.name,data.shares) # ACME 50
	
	# {"__classname__": "JSONObject", "name": "ACME", "shares": 50, "price": 490.1}
	data_str = json.dumps(data,default=JSONObject.serialize)
	print(data_str)
	
	data1 = json.loads(data_str,object_hook=JSONObject.unserialize)
	print(data1.name,data1.shares) # ACME 50
	




if __name__=="__main__":
	try:
	
		# test_json()
		# test_different()
		# test_pprint()
		# convert_2_ordereddict()
		convert_2_pythondict()
	
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




