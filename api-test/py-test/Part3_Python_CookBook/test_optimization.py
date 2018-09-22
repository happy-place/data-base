#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
1) 不要进行全局优化，这样会影响代码可读性，应该先进行性能测试，着重针对瓶颈进行优化
2）不必要的全局代码，建议封装到函数中取执行，因为函数体中的局部变量，要比顶层代码中的全局变量运行更快
3）所有(.) 的操作，都会触发底层的 __getattribute__ 和 __getattr__ 函数调用，在重复循环操作中推荐 通过 val = self.val 方式，先将
实例属性提取，赋值给局部变量，使用局部变量在循环体进行操作
4) from module import name 调用效率比 import module + module.name 调用效率要高。甚至在循环体中可以使用 sqrt = math.sqrt 先将
模块函数对象赋值给局部变量，然后在循环体中调用局部变量，提升效率
5）尽可能使用C语言实现的内置的容器，避免自定义容器
6）应该着重考虑算法层面优化
7）a = {
    'name' : 'AAPL',
    'shares' : 100,
    'price' : 534.22
}

b = dict(name='AAPL', shares=100, price=534.22) 可读性好，效率低
8）借助 JIT 及时编译技术，将频繁执行部分转换为本机机器码，可极大提升效率



"""
import os,traceback





if __name__=="__main__":
	try:
	
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




