#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/25'
Info:
        
"""

import os,traceback
from urllib.request import urlopen
from xml.etree.ElementTree import parse,iterparse,Element,tostring
from collections import Counter
from xml.sax.saxutils import escape, unescape


def test_parse():
	u = urlopen('http://planet.python.org/rss20.xml')
	doc = parse(u)
	
	e = doc.find('channel/description')
	print(e.tag) # description
	print(e.text) # Planet Python - http://planetpython.org/
	# print(e.get('someattribute'))
	
	for item in doc.iterfind('channel/item'):# 从顶层 <rss> 节点先找到<channal>子节点，然后拿到channel 内部全部<item>节点
		title = item.findtext('title')
		date = item.findtext('pubDate')
		link = item.findtext('link')
		
		print(title,date,link)
		'''
		Mike Driscoll: Python 101: Episode #17 – The email and smtp modules Wed, 25 Jul 2018 05:05:29 +0000 http://www.blog.pythonlibrary.org/2018/07/25/python-101-episode-17-the-email-and-smtp-modules/
		Reuven Lerner: Avoiding Windows backslash problems with Python’s raw strings Tue, 24 Jul 2018 18:49:34 +0000 https://blog.lerner.co.il/avoiding-windows-backslash-problems-with-pythons-raw-strings/
		Davy Wybiral: Running python-RQ on a Raspberry Pi 3 Cluster Tue, 24 Jul 2018 17:17:00 +0000 http://davywybiral.blogspot.com/2018/07/running-python-rq-on-raspberry-pi-3.html

		'''

def parse_and_remove(filename,path):
	path_parts = path.split("/")
	doc = iterparse(filename,('start','end'))
	
	next(doc) # 直接跳过root element
	
	tag_stack = []
	elem_stack = []
	
	for event,elem in doc:
		if event =='start':
			tag_stack.append(elem.tag)
			elem_stack.append(elem)
		elif event == 'end':
			if tag_stack == path_parts:
				yield elem
				elem_stack[-2].remove(elem)
			try:
				tag_stack.pop()
				elem_stack.pop()
			except IndexError:
				pass


def dict_2_xml(tag,d):
	elem = Element(tag)
	for k,v in d.items():
		child = Element(k)
		child.text = str(v)
		elem.append(child)
	return elem


def test_dict2xml():
	s = { 'name': 'GOOG', 'shares': 100, 'price':490.1 }
	s = {'name' : '<spam>'}
	elem = dict_2_xml('stock',s)
	print(elem) # <Element 'stock' at 0x1031fa868>
	print(tostring(elem)) # b'<stock><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'
	
	elem.set('_id','1234')
	print(tostring(elem)) # 添加元素 b'<stock _id="1234"><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'


def dict_to_xmlstr(tag,d):
	outer = ["<{parent}>".format(parent=tag),]
	for k,v in d.items():
		outer.append("<{child}>{value}</{child}>".format(child=k,value=v))
	outer.append("</{parent}>".format(parent=tag))
	return ''.join(outer)

def test_dict_to_xmlstr():
	'''
	拼接字典，以str(xml) 格式呈现
	:return:
	'''
	s = { 'name': 'GOOG', 'shares': 100, 'price':490.1 }
	
	elem = dict_to_xmlstr('stock',s)
	print(elem) # <stock><name>GOOG</name><shares>100</shares><price>490.1</price></stock>

def test_update():
	doc = parse('pred.xml') # 读取xml
	root = doc.getroot()
	
	root.remove(root.find('sri'))
	root.remove(root.find('cr'))
	
	root.getchildren().index(root.find('nm'))
	
	e = Element('spam')
	e.text = 'This is a test.'
	root.insert(2,e)
	doc.write('newpred.xml',xml_declaration=True)
	'''
	<?xml version='1.0' encoding='us-ascii'?>
	<stop>
	    <id>14791</id>
	    <nm>Clark &amp; Balmoral</nm>
	    <spam>This is a test.</spam>
	    <pre>
	        <pt>5 MIN</pt>
	        <fd>Howard</fd>
	        <v>1378</v>
	        <rn>22</rn>
	    </pre>
	    <pre>
	        <pt>15 MIN</pt>
	        <fd>Howard</fd>
	        <v>1867</v>
	        <rn>22</rn>
	    </pre>
	</stop>
	'''
	
	
def parse_without_ns():
	doc = parse('ns.xml')
	print(doc.findtext('author'))  # David Beazley
	print(doc.find('content/html')) # None
	print(doc.find('content/{http://www.w3.org/1999/xhtml}html')) # <Element '{http://www.w3.org/1999/xhtml}html' at 0x1065cf688>
	print(doc.findtext('content/{http://www.w3.org/1999/xhtml}html/head/title')) # None
	print(doc.findtext('content/{http://www.w3.org/1999/xhtml}html/{http://www.w3.org/1999/xhtml}head/{http://www.w3.org/1999/xhtml}title')) # Hello World


class XMLNamespaces:
	def __init__(self, **kwargs):
		self.namespaces = {}
		for name, uri in kwargs.items():
			self.register(name, uri)
	def register(self, name, uri):
		self.namespaces[name] = '{'+uri+'}'
	def __call__(self, path):
		return path.format_map(self.namespaces)

def test_ns():
	doc = parse('ns.xml')
	ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')
	print(doc.find(ns('content/{html}html'))) # <Element '{http://www.w3.org/1999/xhtml}html' at 0x102d167c8>
	print(doc.findtext(ns('content/{html}html/{html}head/{html}title'))) # Hello World





if __name__=="__main__":
	try:
		# test_parse()
		# test_dict2xml() # b'<stock><name>&lt;spam&gt;</name></stock>'
		# test_dict_to_xmlstr()
		# test_update()
		# parse_without_ns()
		test_ns()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




