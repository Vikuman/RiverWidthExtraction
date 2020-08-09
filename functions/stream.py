# Modules to import -------------------------------------------------------------------------------
import cv2
from math import floor,sqrt
import csv
import numpy as npy
from functions.river import River
# -------------------------------------------------------------------------------------------------

# Class - Stream ----------------------------------------------------------------------------------
class Stream:
	# Class variables -------------------------------------------------------------------
	point=(0,0) # position of the Stream type variable	
	DistanceFromReachStart=0 # distance of the stream point from the starting point of the reach which contains it
	width=0 # river width across that stream point
	slope=0  # slope of perpendicular
	greenLeft=(0,0) # left green Line coordinates (coordinates of the boundary points across that stream point)
	greenRight=(0,0) # right green Line coordinates (coordinates of the boundary points across that stream point)
	isGood=False # check if the width was calculated
	Discharge=0 # not needed
	list_single_stream_coordinates =[]
	number_of_pixels = 0
	# -----------------------------------------------------------------------------------

	# Constructor function --------------------------------------------------------------
	def __init__(self,pos):
		# Initialize the variables
		self.point=pos
		self.DistanceFromReachStart=0
		self.width=-1
		self.slope=0
		self.greenLeft=(0,0)
		self.greenRight=(0,0)
		self.isGood=False
		self.Discharge=0
		self.list_single_stream_coordinates =[]
		self.number_of_pixels = 0

		return
	# -----------------------------------------------------------------------------------


	# Class Functions -------------------------------------------------------------------
	# Return the position of the stream point ---------------------------------
	def getLocation(self):
		return self.point
	# -------------------------------------------------------------------------


	# Set the DistanceFromReachStart value to val, for a given stream point ---
	def setDistanceFromStart(self,val):
		self.DistanceFromReachStart=val
		return
	# -------------------------------------------------------------------------


	# Set values of the class variable as per the given parameters ------------
	def setValues(self,width,slope,left,right):
		self.width=width
		self.slope=slope
		self.greenLeft=left
		self.greenRight=right
		self.isGood=True
		# Below we need to use the formula for discharge calculation
		# self.Discharge = (npy.sqrt(9.8*(190e-6))*(width)**2)/4 # threshold theory based
		# self.Discharge = (npy.sqrt(9.8*(190e-6)**5)*(width/(190e-6))**1.73)/0.27  # emperical relation
		self.Discharge = ((width)**2)/100  # exponent is same (0.5) and prefacture is adjusted to see the best fit
		return
	# -------------------------------------------------------------------------


	# Draw green lines perpendicular to the stream points ---------------------
	def Draw(self,a_Image,color,list_all_green_lines):
		if not self.isGood:
			return
		else:
			x1 = self.greenLeft[0]
			y1 = self.greenLeft[1]
			x2 = self.greenRight[0]
			y2 = self.greenRight[1]
			self.number_of_pixels = int(floor(sqrt((x2-x1)**2 + (y2-y1)**2)))
			self.list_single_stream_coordinates.append(list(self.greenLeft))
			self.list_single_stream_coordinates.append(list(self.greenRight))
			self.list_single_stream_coordinates.append(self.number_of_pixels)
			list_all_green_lines.append(self.list_single_stream_coordinates)
			cv2.line(a_Image,self.greenLeft,self.greenRight,color)
			return
	# -------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------


	# Not Needed ------------------------------------------------------------------------
	"""
	def printInfo(self):
		print ("At position",self.point,",Width=",self.width,",Distance From Start=",self.DistanceFromReachStart)
		return

	def getDistanceFromStart(self):
		return self.DistanceFromReachStart

	def getWidth(self):
		return self.width
	"""
# End of class ------------------------------------------------------------------------------------