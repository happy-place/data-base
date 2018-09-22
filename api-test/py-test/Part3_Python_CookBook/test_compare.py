#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
from functools import total_ordering

class Room:
	def __init__(self,name,lenght,width):
		self.name = name
		self.length = lenght
		self.width = width
		self.square_feet = lenght * width
	
@total_ordering
class House:
	'''
	只需要在House 中定义 __eq__ __lt__ 方法，就可以基于@total_ordering 注解，自动补全其余 __le__ ge__ 方法，
	并且可以基于 > < = 进行比较
	'''
	
	def __init__(self,name,style):
		self.name = name
		self.style = style
		self.rooms = list()
	
	@property
	def living_space_footage(self):
		return sum(r.square_feet for r in self.rooms)
	
	def add_room(self,room):
		self.rooms.append(room)

	def __str__(self):
		return '{}: {} square foot {}'.format(self.name,self.living_space_footage,self.style)

	def __eq__(self,other):
		return self.living_space_footage == other.living_space_footage

	def __lt__(self,other):
		return self.living_space_footage < other.living_space_footage


def test_ordering():
	h1 = House('h1', 'Cape')
	h1.add_room(Room('Master Bedroom', 14, 21))
	h1.add_room(Room('Living Room', 18, 20))
	h1.add_room(Room('Kitchen', 12, 16))
	h1.add_room(Room('Office', 12, 12))
	
	h2 = House('h2', 'Ranch')
	h2.add_room(Room('Master Bedroom', 14, 21))
	h2.add_room(Room('Living Room', 18, 20))
	h2.add_room(Room('Kitchen', 12, 16))
	
	h3 = House('h3', 'Split')
	h3.add_room(Room('Master Bedroom', 14, 21))
	h3.add_room(Room('Living Room', 18, 20))
	h3.add_room(Room('Office', 12, 16))
	h3.add_room(Room('Kitchen', 15, 17))
	
	houses = [h1, h2, h3]
	
	print('Is h1 bigger than h2?', h1 > h2) # prints True
	print('Is h2 smaller than h3?', h2 < h3) # prints True
	print('Is h2 greater than or equal to h1?', h2 >= h1) # Prints False
	print('Which one is biggest?', max(houses)) # Prints 'h3: 1101-square-foot Split'
	print('Which is smallest?', min(houses)) # Prints 'h2: 846-square-foot Ranch'






if __name__=="__main__":
	try:
		test_ordering()
		
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




