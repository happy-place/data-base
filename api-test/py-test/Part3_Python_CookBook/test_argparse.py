#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
import argparse


def create_parser():
	# 脚本功能描述
	parser = argparse.ArgumentParser(description='Search some files')
	
	# 输入文件名，可以穿多个
	parser.add_argument(dest='filenames',metavar='filename', nargs='*')
	
	# 模式 必须的，最终映射到 dest 属性上 ，并追加到列表中，显示帮助信息时 help
	parser.add_argument('-p', '--pat',metavar='pattern', required=True,
	                    dest='patterns', action='append',
	                    help='text pattern to search for')
	
	# 存储一个 boolean 类型变量到字典
	parser.add_argument('-v', dest='verbose', action='store_true',
	                    help='verbose mode')
	
	# 输出
	parser.add_argument('-o', dest='outfile', action='store',
	                    help='output file')
	
	# 速率
	parser.add_argument('--speed', dest='speed', action='store',
	                    choices={'slow','fast'}, default='slow',
	                    help='search speed')
	
	args = parser.parse_args()
	
	# Output the collected arguments
	print('filenames: ',args.filenames)
	print('patterns: ',args.patterns)
	print('verbose: ',args.verbose)
	print('outfile: ',args.outfile)
	print('speed: ',args.speed)

create_parser()


# python3 test_argparse.py -h 查看帮助
'''
usage: test_argparse.py [-h] -p pattern [-v] [-o OUTFILE]
                        [--speed {fast,slow}]
                        [filename [filename ...]]

Search some files

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  -p pattern, --pat pattern
                        text pattern to search for
  -v                    verbose mode
  -o OUTFILE            output file
  --speed {fast,slow}   search speed
  
'''

# python3 test_argparse.py -v -p spam --pat=eggs foo.txt -o results --speed=fast
'''
filenames:  ['foo.txt']
patterns:  ['spam', 'eggs']
verbose:  True
outfile:  results
speed:  fast
'''

# if __name__=="__main__":
# 	try:
# 		create_parser()
# 		pass
# 	except:
# 		traceback.print_exc()
# 	finally:
# 		os._exit(0)




