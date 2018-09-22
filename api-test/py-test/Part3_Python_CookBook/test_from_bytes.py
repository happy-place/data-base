#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,struct


def test_pack():
	'''
	将128位长的16个元素的字节字符串解析层10进制整型
	:return:
	'''
	data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004' # 字节字符串
	print(len(data)) # 16
	print(int.from_bytes(data,'little')) # 69120565665751139577663547927094891008
	print(int.from_bytes(data,'big')) # 94522842520747284487117727783387188
	
	print(int(94522842520747284487117727783387188).to_bytes(16,'big')) # b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
	print(int(69120565665751139577663547927094891008).to_bytes(16,'little')) # b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'

def test_struct():
	'''
大整数和字节字符串之间的转换操作并不常见。然而，在一些应用领域有时候也会 出现，比如密码学或者网络。例如，IPv6 网络地址使用一个 128 位的整数表示。如果 你要从一个数据记录中提取这样的值的时候，你就会面对这样的问题。
作为一种替代方案，你可能想使用 6.11 小节中所介绍的 struct 模块来解压字节。 这样也行得通，不过利用 struct 模块来解压对于整数的大小是有限制的。因此，你可 能想解压多个字节串并将结果合并为最终的结果，就像下面这样:
	:return:
	'''
	
	# struct 将长字节字符串解析成高低位字符串，然后通过位移拼接即可恢复
	data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004' # 字节字符串
	hi,lo = struct.unpack('>QQ',data)
	print((hi<<64) + lo) # 94522842520747284487117727783387188
	
	x = 0x01020304
	print(x.to_bytes(4,'big')) # b'\x01\x02\x03\x04'
	print(x.to_bytes(4,'little')) # b'\x04\x03\x02\x01'
	
	pass

def test_to_bytes():
	x = 523**23
	base = 8
	
	'''
	x.bit_length() 得到存储x需要的二进制位数，如果不能整除则 +8bit
	'''
	nbytes,rem = divmod(x.bit_length(),8)
	if rem :
		nbytes +=1
	else:
		# To save 335381300113661875107536852714019056160355655333978849017944067 base on 8, need 26 bytes (208 bits) > 208
		print('To save {x} base on {base}, need {num} bytes ({bits} bits) > {total}'.format(x=x,base=base,num=nbytes,bits=nbytes*8,total=x.bit_length()))
			
	# b'\x03X\xf1\x82iT\x96\xac\xc7c\x16\xf3\xb9\xcf\x18\xee\xec\x91\xd1\x98\xa2\xc8\xd9R\xb5\xd0'
	print(x.to_bytes(nbytes,'little')) # 按指定位数存储


if __name__=="__main__":
	try:
		# test_pack()
		# test_struct()
		test_to_bytes()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)
