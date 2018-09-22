#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback,shutil

def copy():
	# 仅拷贝文件内容
	base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
	shutil.copy(base+'aa/1.txt',base+'bb/1.txt')

def copy_with_meta():
	# 拷贝 内容同时，还拷贝元数据
	base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
	shutil.copy2(base+'aa/1.txt',base+'bb/2.txt')

def copy_dir():
	# 递归拷贝文件目录，并且维持元数据
	base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
	shutil.copytree(base+'bb',base+'cc')

def move():
	# 移动
	base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
	shutil.move(base+'cc/2.txt',base+'aa')

def copy_with_link():
	# 拷贝文件目录，并保持超链接
	base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
	shutil.copytree(base+'aa',base+'cc',symlinks=True)

def ignore_pyc(dirname,filenames):
	return [name for name in filenames if name.endswith('.py')]

def copy_ignore():
	base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
	shutil.copytree(base+'aa',base+'cc',ignore=ignore_pyc) # 目录 和 目录下文件，作为入参，传递给ignore_pyc

def test_os():
	filename = '/Users/huhao/Desktop/mix_predict.py'
	dirname=os.path.dirname(filename)
	print(dirname) # /Users/huhao/Desktop
	
	fname = os.path.basename(filename)
	print(fname) # mix_predict.py
	
	d,f = os.path.split(filename)
	print(d,f) # /Users/huhao/Desktop mix_predict.py
	
	new_path = os.path.join('~',os.path.basename(filename))
	print(new_path) # ~/mix_predict.py
	
	fullname = os.path.expanduser(new_path)
	print(fullname) # /Users/huhao/mix_predict.py

def rec_error():
	try:
		base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
		shutil.copytree(base+'aa',base+'cc') # 目录 和 目录下文件，作为入参，传递给ignore_pyc
	except shutil.Error as e: # 拷贝失败时会将失败信息记录在e 中
		for src,dst,msg in e.args[0]:
			print(dst,src,msg)

def test_mk_archive():
	archive_formats = shutil.get_archive_formats()
	print(archive_formats) # [('bztar', "bzip2'ed tar-file"), ('gztar', "gzip'ed tar-file"), ('tar', 'uncompressed tar file'), ('xztar', "xz'ed tar-file"), ('zip', 'ZIP file')]
	
	base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
	shutil.make_archive('aa','zip',base+'aa')  # make_archive(目标文件名,归档格式,待归档文件目录) # 压缩


def test_unpack_archive():
	base = '/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part3_Python_CookBook/'
	shutil.unpack_archive(base+'aa.zip',base+'aa_bk') # unpack_archive(待解压文件，解压到的目录)


if __name__=="__main__":
	try:
		# copy()
		# copy_with_meta()
		# copy_dir()
		# move()
		# copy_with_link()
		# copy_ignore()
		# test_os()
		# test_mk_archive()
		test_unpack_archive()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




