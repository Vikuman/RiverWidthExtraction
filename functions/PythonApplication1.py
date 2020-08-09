# Modules to import -----------------------------------------------------------
from osgeo import gdal
from osgeo import osr
import simplekml
from math import sin, cos, sqrt, atan2, radians
from skimage import morphology
import cv2
import csv

import numpy as npy
from matplotlib import pyplot as plt 
from PIL import Image as image

from scipy import ndimage 
from scipy.stats import describe
from pylab import*
import glob, os
#import MySQLdb as msql
import operator 
import itertools
import copy
from datetime import datetime
from functions.river import River
from functions.Skeleton import Skeleton
from functions.scan import Scan
# from pixel_to_coordinates import pixel2coord
import sys
import base64
import math

import PIL
import PIL.Image, PIL.ImageFile
# -----------------------------------------------------------------------------


# Global Variables ------------------------------------------------------------
rcParams['lines.markersize']=10
rcParams['lines.linewidth'] = 11
rcParams['font.size']=11
rcParams['xtick.labelsize']=11
rcParams['ytick.labelsize']=11
rcParams['legend.fontsize']=11
rcParams['patch.linewidth'] = 1. # this is for the edges of markers
rcParams['axes.linewidth'] = 1.
rcParams['xtick.major.pad'] = 11

BLACK=0
WHITE=255
BLUE=100
rgbRED=[255.0,0.0,0.0]
rgbBLUE=[0.0,0.0,255.0]
rgbGREEN=[0.0,102.0,0.0]
rgbYELLOW=[255.0,255.0,0.0]
rgbBLACK=[0.0,0.0,0.0]
rgbWHITE=[255.0,255.0,255.0]
rgbCYAN=[0.0,255.0,255.0]
rgbSAFFRON=[255.0,128.0,0]
rgbPINK=[255.0,192.0,0]
rgbGRAY=[192,192,192]
NOTUSED = -1234

def saveJPG(img,filename):
	plt.imshow(img)
	plt.savefig(filename, format = 'jpg', dpi=1200)
# -----------------------------------------------------------------------------
def pixel2coord(col, row ,ds):
	l=[]
	
	c, a, b, f, d, e = ds.GetGeoTransform()

	"""Returns global coordinates to pixel center using base-0 raster index"""
	xp = a * (col) + b * (row) + a * 0.5 + b * 0.5 + c
	yp = d * (col) + e * (row) + d * 0.5 + e * 0.5 + f
	var = str(xp)+","+str(yp)
	l.append(xp)
	l.append(yp)
	
	return(l)

# -----------------------------------------------------------------------------

def cartesian_to_tiff_coordinates(input_file_name,output_file_name,name_of_file,name_id):
	fields = []
	rows = []
	final_list=[]
	variable=""
	ds = gdal.Open(name_of_file)
	with open(input_file_name) as f:
		count=0
		reader = csv.reader(f)
		a=list(reader)
		for row in reader:
			rows.append(row)
		for i in range(len(a)):
			list_one=[]
			for j in range(len(a[i])-1):
				count+=1
				pixels = int(a[i][2])
				x_coord = float((a[i][j].replace("[","").replace("]","")).split(",")[0])
				y_coord = float((a[i][j].replace("[","").replace("]","")).split(",")[1])
				
				if (input_file_name == name_id + "stream-lines.csv") :
					list_one.append(pixel2coord(x_coord,y_coord ,ds))
					if j==1:
						list_one.append(pixels)
				else:
					list_one.append(pixel2coord(y_coord,x_coord ,ds))	
			final_list.append(list_one)			
	f.close()		
	with open (output_file_name,"+w") as fi:
		writer = csv.writer(fi)
		writer.writerows(final_list)
	fi.close()
	return



# -----------------------------------------------------------------------------
def tiff_to_kml(input_file,output_file,name_of_file,name_id):
	final_list=[]
	var = 0
	dist = 0
	latlong =""
	kml = simplekml.Kml()
	ds = gdal.Open(name_of_file)
	old_cs= osr.SpatialReference()
	old_cs.ImportFromWkt(ds.GetProjectionRef())
	wgs84_wkt = """
	GEOGCS["WGS 84",
		DATUM["WGS_1984",
			SPHEROID["WGS 84",6378137,298.257223563,
				AUTHORITY["EPSG","7030"]],
			AUTHORITY["EPSG","6326"]],
		PRIMEM["Greenwich",0,
			AUTHORITY["EPSG","8901"]],
		UNIT["degree",0.01745329251994328,
			AUTHORITY["EPSG","9122"]],
		AUTHORITY["EPSG","4326"]]"""
	new_cs = osr.SpatialReference()
	new_cs .ImportFromWkt(wgs84_wkt)
	transform = osr.CoordinateTransformation(old_cs,new_cs) 
	width = ds.RasterXSize
	height = ds.RasterYSize
	gt = ds.GetGeoTransform()
	minx = gt[0]
	miny = gt[3] + width*gt[4] + height*gt[5] 
	with open(input_file) as f:
		reader = csv.reader(f)
		a=list(reader)
		for i in a:
			list_one =[]
			l = 0
			dist = 0
			pixels =""
			for j in i :
				if j.startswith("["):
					latlong = transform.TransformPoint(float(j.replace("]","").replace("[","").split(",")[0]),float(j.replace("]","").replace("[","").split(",")[1]))
					list_one.append(latlong[0])
					list_one.append(latlong[1])
				else:
					pixels =j
			lon1 = radians(float(list_one[0]))
			lat1 = radians(float(list_one[1]))
			lon2 = radians(float(list_one[2]))
			lat2 = radians(float(list_one[3]))
			dlon = lon2 - lon1
			dlat = lat2 - lat1
			q = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
			c = 2 * atan2(sqrt(q), sqrt(1 - q))
			d = 6373.0 * c				#(where 6373 is the radius of the Earth) The values used for the radius of the Earth (3961 miles & 6373 km) are optimized for locations around 39 degrees from the equator (roughly the Latitude of Washington, DC, USA).
			kml.newlinestring(name = "Stream-Line :" + "no. of pixels contained:" + str(pixels), description = str(d)+" in Km").coords = [(list_one[0],list_one[1]),(list_one[2],list_one[3])]
	f.close()
	kml.save(output_file)
	return 	





# The main fucntion -------------------------------------------------------------------------------
def main(encoded_string,name_id,thresh,scale,len_dang_arcs,section_size):
	# Initialize the variables ----------------------------------------------------------
	#name_id="jdbjdsbhjcbdshbc"
	# thresh = 0
	# scale = 10
	# interval_distance = 200
	# len_dang_arcs = 100
	name_of_file = ""
	interval_distance = section_size
	l_r_error = 8
	final_average_width = 0
	list_all_green_lines =[]
	# -----------------------------------------------------------------------------------


	# Save the encoded image by the name of the process-id ------------------------------
	pid_name = str(os.getpid())
	with open('pid_' + pid_name + '.png', "wb") as fh:
	    fh.write(base64.b64decode(encoded_string))
	# -----------------------------------------------------------------------------------
	with open('pid_' + pid_name + '.tif', "wb") as ft:
		ft.write(base64.b64decode(encoded_string))
	name_of_file = 'pid_' + pid_name + '.tif'
	# Load the image into a cv2.imread() variable, in grey scale mode -------------------
	img = cv2.imread('pid_' + pid_name + '.png',0)
	# -----------------------------------------------------------------------------------


	# Delete the image ------------------------------------------------------------------
	my_path = os.getcwd() # get the path to current directory - ...\myProject\myProject
	os.unlink('pid_' + pid_name+ '.png') # delete the image
	# -----------------------------------------------------------------------------------


	# Calculate the average width -------------------------------------------------------
	river = River(img,thresh,math.floor(interval_distance/scale),0) # process the river image
	skeleton = Skeleton(river,math.floor(len_dang_arcs/scale),0) # find the skeleton, junctions and reaches
	scan = Scan(river,skeleton,l_r_error) # create a new Scan type object and run Compute() on it 
	scan.Compute()

	l2_stream = scan.getAllStreamFromReach(scan.l_reaches) # create a list of all the lists of stream points
	scan.averageCalculation(math.floor(interval_distance/scale),l2_stream) # calculate the average width of the river (section by section also)
	final_average_width = scan.average_width_river # store the average width into the variable - final_average_width

	print(final_average_width*scale, " <- Average width of the river")
	# -----------------------------------------------------------------------------------


	# Write the details to the text file ------------------------------------------------
	details='---------- This file contains the details of the river image analysed ----------\n\n\n'
	details+='Threshold value used : '+str(river.threshold_value)+'\n'
	details+='Scale value used : '+str(scale)+'\n'
	details+='Interval distance selected : '+str(interval_distance)+'\n'
	details+='Length of permissible dangling segments : '+str(len_dang_arcs)+'\n'
	details+='Number of junctions : '+str(len(skeleton.list_Junction)-2)+'\n'
	details+='Number of reaches : '+str(len(skeleton.l_Reach)-1)+'\n'
	details+='Average width of the river : '+str(scan.average_width_river*scale)+'\n\n\n'
	details+='Data about the sections ----------------------------------------\n\n'
	for x in range(len(scan.l_average_width_section)):
		details+='Section '+str(x+1)+' -------------------------\n'
		details+='     Starting Distance : '+str(x*interval_distance)+'\n'
		details+='     Number of channels : '+str(scan.l_channels[x])+'\n'
		details+='     Average width : '+str(scan.l_average_width_section[x]*scale)+'\n\n'

	# with open('output_details.txt', 'w') as write_file :
	# 	write_file.write(details)
	# -----------------------------------------------------------------------------------


	# Display the reference image -------------------------------------------------------
	a_Image = scan.getNullFigure() # create a figure with all of its pixels - 0
	a_Image.fill(255) # fill all the pixels with - 1

	scan.drawRiverContour(a_Image,rgbBLUE) # draw the river contours
	scan.drawSkeleton(a_Image,rgbBLACK,rgbBLACK) # draw the skeleton
	scan.drawJunction(a_Image,rgbRED) # draw the junctions
	scan.drawStream(a_Image,l2_stream,rgbGREEN,list_all_green_lines) # draw the green lines across all stream points

	plt.figure(1) # create a new figure
	plt.imshow(a_Image) # draw a_Image on the current figure
	plt.show() # display the figure
	# -----------------------------------------------------------------------------------





	save_path='/home/vikuman/Desktop/iiserupdated/DjangoWebProject1/media/'
	# complete_name=os.path.join(save_path,name_id+".csv")
	# download_path=os.path.join("/text_result",name_id+".csv")
	# print("download path=",download_path)

	with open(name_id + "stream-lines.csv", "+w") as f:
	# f=open(complete_name,"w+")

	# f.write(details)
		writer = csv.writer(f)
		writer.writerows(list_all_green_lines)
	f.close()















	# path="/home/sanjeev/Desktop/final/iiserupdated/DjangoWebProject1/media/"
	# name_of_figure = name_id + ".png"
	# plt.savefig(path + name_of_figure)

	# with open(name_id + ".csv", "+w") as f:
	# 	writer = csv.writer(f)
	# 	writer.writerows(list_all_green_lines)
	# f.close()	
	
	plt.show() # display the figure

	# cartesian_to_tiff_coordinates("skeleton_with_arcs.csv","skeleton_with_arc_tiff_coordinates.csv")
	# cartesian_to_tiff_coordinates("skeleton_without_arcs.csv","skeleton_without_arc_tiff_coordinates.csv")
	cartesian_to_tiff_coordinates(name_id + "stream-lines.csv",name_id + "stream_points_tiff_coordinates.csv",name_of_file,name_id)


	# tiff_to_kml("skeleton_with_arc_tiff_coordinates.csv","skeleton_with_arc.kml")
	# tiff_to_kml("skeleton_without_arc_tiff_coordinates.csv","skeleton_without_arc.kml")
	# tiff_to_kml(name_id + "stream_points_tiff_coordinates.csv",name_id + "stream_points.kml",name_of_file,name_id)


	# Delete the image ------------------------------------------------------------------
	my_path = os.getcwd() # get the path to current directory - ...\myProject\myProject
	os.unlink('pid_' + pid_name+ '.tif') # delete the image
	# -----------------------------------------------------------------------------------

	return final_average_width*scale,details # return the average width
# -------------------------------------------------------------------------------------------------





# To be removed -------------------------------------------------------------------------
"""
from WidthExtraction import main
final_average_width = main()
print(final_average_width)
"""
# ---------------------------------------------------------------------------------------
