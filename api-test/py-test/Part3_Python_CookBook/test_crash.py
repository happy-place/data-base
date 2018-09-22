#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,sys,pdb

# 方案1；直接在 python3 命令行调脚本，然后通过 pdb 模块，进行栈内调试
def func(n):
	return n+10
	'''
	>>> import pdb
	>>> pdb.pm()
	> sample.py(4)func()
	-> return n + 10
	(Pdb) w
	  sample.py(6)<module>()
	-> func('Hello')
	> sample.py(4)func()
	-> return n + 10
	(Pdb) print n  《《《《
	'Hello'
	(Pdb) q
	>>>
	'''

# 方案2：在目标函数调用逻辑上使用 try_catch 机制，借助 traceback.print_exc(file=sys.stderr) 进行追踪
def func2(n):
	try:
		print(func(n))
	except:
		print('******An Error Occured ******')
		traceback.print_exc(file=sys.stderr)
		'''
		******An Error Occured ******
		Traceback (most recent call last):
		  File "/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/test_crash.py", line 33, in func2
		    print(func(n))
		  File "/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/test_crash.py", line 14, in func
		    return n+10
		TypeError: must be str, not int
		
		'''

# 方案3：与预期补一致时，直接调用 traceback.print_stack(file=sys.stderr) 从开始调用，至traceback.print_stack 所在位置停止
def func3(n):
	if n>10:
		print(func(n))
	else:
		traceback.print_stack(file=sys.stderr)
	'''
	  File "/Users/huhao/Library/Application Support/IntelliJIdea2017.3/python/helpers/pydev/pydev_run_in_console.py", line 151, in <module>
        globals = run_file(file, None, None, is_module)
	  File "/Users/huhao/Library/Application Support/IntelliJIdea2017.3/python/helpers/pydev/pydev_run_in_console.py", line 53, in run_file
	    pydev_imports.execfile(file, globals, locals)  # execute the script
	  File "/Users/huhao/Library/Application Support/IntelliJIdea2017.3/python/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
	    exec(compile(contents+"\n", file, 'exec'), glob, loc)
	  File "/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/test_crash.py", line 61, in <module>
	    func3(5)
	  File "/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/test_crash.py", line 53, in func3
	    traceback.print_stack(file=sys.stderr)
	
	'''

def func4(n):
	a = n+1
	pdb.set_trace()
	b = a -2
	pdb.set_trace()



if __name__=="__main__":
	try:
		# func('hello')
		# func2('heoo')
		# func3(5)
		func4(2)
		pass
	except:
		traceback.print_stack(file=sys.stderr)
	finally:
		os._exit(0)



