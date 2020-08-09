# Modules to import -------------------------------------------------------------------------------
import os
import cv2
import math
import base64
from matplotlib import pyplot as plt
from functions.river import River
from functions.Skeleton import Skeleton
from functions.scan import Scan
# -------------------------------------------------------------------------------------------------


# Global Variables --------------------------------------------------------------------------------
rgbRED=[255.0,0.0,0.0]
rgbBLUE=[0.0,0.0,255.0]
rgbGREEN=[0.0,255.0,0.0]
rgbYELLOW=[255.0,255.0,0.0]
rgbBLACK=[0.0,0.0,0.0]
rgbWHITE=[255.0,255.0,255.0]
rgbCYAN=[0.0,255.0,255.0]
rgbSAFFRON=[255.0,128.0,0]
rgbPINK=[255.0,192.0,0]
# -------------------------------------------------------------------------------------------------


# The main fucntion -------------------------------------------------------------------------------
def main(encoded_string,name_id,thresh,scale,len_dang_arcs,section_size):
	# Initialize the variables ----------------------------------------------------------
	#name_id="jdbjdsbhjcbdshbc"
	# thresh = 0
	# scale = 10
	# interval_distance = 200
	# len_dang_arcs = 100
	interval_distance = section_size
	l_r_error = 8
	final_average_width = 0
	# -----------------------------------------------------------------------------------


	# Save the encoded image by the name of the process-id ------------------------------
	pid_name = str(os.getpid())
	with open('pid_' + pid_name + '.png', "wb") as fh:
	    fh.write(base64.b64decode(encoded_string))
	# -----------------------------------------------------------------------------------


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
	scan.drawStream(a_Image,l2_stream,rgbGREEN) # draw the green lines across all stream points

	plt.figure(1) # create a new figure
	plt.imshow(a_Image) # draw a_Image on the current figure
	plt.show() # display the figure
	# -----------------------------------------------------------------------------------
	path="/home/sanjeev/Desktop/final/iiserupdated/DjangoWebProject1/media/"
	name_of_figure = name_id + ".png"
	plt.savefig(path + name_of_figure)

	return final_average_width*scale,details # return the average width
# -------------------------------------------------------------------------------------------------





# To be removed -------------------------------------------------------------------------
"""
from WidthExtraction import main
final_average_width = main()
print(final_average_width)
"""
# ---------------------------------------------------------------------------------------
