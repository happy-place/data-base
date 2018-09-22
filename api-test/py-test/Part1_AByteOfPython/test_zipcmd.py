#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/16'
Info:
        
"""
import os,time,traceback



if __name__=="__main__":
	sources = ["/Users/huhao/Desktop/aa","/Users/huhao/Desktop/bb"]
	dest_dir = "/Users/huhao/Desktop/backup/"
	try:
		zip_name = str(input("Please Enter zip_file name: "))
		print(zip_name)
		if len(zip_name)==0:
			dest = dest_dir +os.sep+time.strftime("%Y%m%d%H$M%S")+".zip"
		else:
			dest = dest_dir +zip_name+"_"+os.sep+time.strftime("%Y%m%d%H$M%S")+".zip"
		
		if not os.path.exists(dest_dir):
			os.mkdir(dest_dir)
			print("Successfully mkdir {dest_dir}".format(dest_dir=dest_dir))
		
		zip_command = "zip -qr {dest} {sources}".format(dest=dest,sources=" ".join(sources))
	
		if os.system(zip_command) == 0 :
			print("Successfully backup {sources} to {dest}".format(dest=dest,sources=" ".join(sources)))
		else:
			print("Fail to backup {sources} to {dest}".format(dest=dest,sources=" ".join(sources)))
	except:
		traceback.print_exc()

	finally:
		os._exit(0)



