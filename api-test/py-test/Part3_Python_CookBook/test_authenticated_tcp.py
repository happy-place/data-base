#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
基本原理是当连接建立后，服务器给客户端发送一个随机的字节消息（这里例子中使用了 os.urandom() 返回值）。
客户端和服务器同时利用hmac和一个只有双方知道的密钥来计算出一个加密哈希值。然后客户端将它计算出的摘要发送给服务器，
服务器通过比较这个值和自己计算的是否一致来决定接受或拒绝连接。摘要的比较需要使用 hmac.compare_digest() 函数。
使用这个函数可以避免遭到时间分析攻击，不要用简单的比较操作符（==）。
 为了使用这些函数，你需要将它集成到已有的网络或消息代码中。

        
"""
import os,hmac

# 只在 首次 调用时延签一次，构建加密连接后，直接传输数据即可
def client_authenicate(connection,secret_key):
	# 接受服务端 32 位 随机加密盐值
	message = connection.recv(32)
	
	hash = hmac.new(secret_key,message)
	digest = hash.digest()
	connection.send(digest)
	
# 服务端调用
def server_authenticate(connection,secret_key):
	# 基于系统生成 32 位长度随机数，作为加密盐值
	message = os.urandom(32)
	# 向客户端发送此随机数
	connection.send(message)
	# 基于加密字符串和盐值，创建解密 digest
	hash = hmac.new(secret_key,message)
	digest = hash.digest()
	# 定长接受客户端传入 数据
	response = connection.recv(len(digest))
	# 完成解密
	return hmac.compare_digest(digest,response)


__all__ = ['client_authenicate','server_authenticate']


