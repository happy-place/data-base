#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/18'
Info:
        
"""
import os
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.misc import imread, imresize


def print_sin():
	# 画图
	x = np.arange(0, 3 * np.pi, 0.1) # x[0,3pi], y:0.1
	y = np.sin(x)
	
	# Plot the points using matplotlib
	plt.plot(x, y)
	plt.show()

def print_sin_cos():
	x = np.arange(0, 3 * np.pi, 0.1)
	y_sin = np.sin(x)
	y_cos = np.cos(x)
	
	# Plot the points using matplotlib
	plt.plot(x, y_sin)
	plt.plot(x, y_cos)
	plt.xlabel('x axis label')
	plt.ylabel('y axis label')
	plt.title('Sine and Cosine')
	plt.legend(['Sine', 'Cosine'])
	plt.show()

def print_subplots():
	# Compute the x and y coordinates for points on sine and cosine curves
	x = np.arange(0, 3 * np.pi, 0.1)
	y_sin = np.sin(x)
	y_cos = np.cos(x)
	
	# Set up a subplot grid that has height 2 and width 1,
	# and set the first such subplot as active.
	plt.subplot(2, 1, 1) # 高 2cm 长1cm (进度0.1cm) 占据第一幅
	
	# Make the first plot
	plt.plot(x, y_sin)
	plt.title('Sine')
	
	# Set the second subplot as active, and make the second plot.
	plt.subplot(2, 1, 2) # 高 2cm 长1cm (进度0.1cm) 占据第二幅
	plt.plot(x, y_cos)
	plt.title('Cosine')
	
	# Show the figure.
	plt.show()


if __name__=="__main__":
	try:
		
		# print_sin()
		# print_sin_cos()
		# print_subplots()
		
	

		pass
	
	finally:
		os._exit(0)
