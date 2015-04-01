#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime
import cv2
import math
import sys
import copy
import os
import argparse

class TimesApproximator(object):
	def __init__(self):
		self.cap = None
		self.info_file = sys.argv[1].split('.')[0][:-9] + "_info.dat"
		self.times_file = sys.argv[1].split('.')[0][:-9] + "_times.dat"
		
		self.start_time = None
		self.end_time = None
		self.time_diff = None
	
	def run(self):
		self.cap = cv2.VideoCapture(sys.argv[1])
		frame_counter = 0
		
		print "Frame times approximation started"
		
		try:
			with open(self.info_file, 'r') as tf:
				self.start_time = datetime.strptime(tf.readline()[12:].rstrip(), '%Y-%m-%d  %H:%M:%S:%f')
				self.end_time = datetime.strptime(tf.readline()[11:].rstrip(), '%Y-%m-%d %H:%M:%S:%f')
		except:
			print "info file missing or badly formatted - can not approximate without start and end time"
			exit()
		
		time_diff = self.end_time - self.start_time
		time_diff_ms = time_diff.seconds*1000000 + time_diff.microseconds
		print time_diff_ms
		
		while self.cap.isOpened() and frame_counter < 50:
			frame_counter += 1
			
			ret, frame = self.cap.read()
			
			#cv2.imshow("frame", frame)
			#cv2.waitKey(1)
		self.cap.release()
		
		print "frames:" + str(frame_counter)
		
		
		
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='approximate frametimes for VideoRecorder')
	parser.add_argument('path', type=str, help="absolute file path to VideoRecorder video including file name and file extension")
    
	args = parser.parse_args()
	if not os.path.exists(args.path):
		print('Video file does not exist!')
		exit()
	
	approx = TimesApproximator()
	approx.run()
    
    