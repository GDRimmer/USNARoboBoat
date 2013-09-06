#Color Tracker (Blue)
#Adapted From Code Found at:http://aravindc.com/2012/12/26/color-tracking-opencv-python-and-my-first-post/
#MIDN Gerald D. Rimmer
#Last Edit: 27 AUG 2013
####################################################################################
from cv import *
####################################################################################
#This function creates a binary image of all pixels in the blue HSV threshold range
#for the color blue
def GetThresholdedImage(img):
	#Create a placeholder for HSV image from camera stream
	imgHSV = CreateImage(GetSize(img), 8, 3)
	#Change from BGR scheme to HSV
	CvtColor(img, imgHSV, CV_BGR2HSV)
	#Create a placeholder for thresholded image
	imgThreshed = CreateImage(GetSize(img), 8, 1)
	#Isolated blue pixels from HSV image and returns them as "high" bianry
        #values (1) or white of the image
	InRangeS(imgHSV, (100, 94, 84), (109, 171, 143), imgThreshed)
	return imgThreshed
####################################################################################
#Define Main() function, this runs all of the tracking protocols
def main():
	#Name display windows
	color_tracker_window = "output"
	thresh_window = "thresh"
	#Capature video stream from camera
	capture = CaptureFromCAM(0)
	NamedWindow( color_tracker_window, 1)
	NamedWindow( thresh_window, 1)
	imgScrible = None
	#Initialize position variables
	posX = 0
	posY = 0
	#Begin Main loop	
	while True:
		#Get video frame from camera
		frame = QueryFrame(capture)
		#Smooth image
		Smooth(frame, frame, CV_BLUR, 3)
		#If track like does not exist yet, create one
		if(imgScrible is None):
			imgScrible = CreateImage(GetSize(frame), 8, 3)
		#Reassign thresholded image to a place holder called BlueThresh
		imgBlueThresh = GetThresholdedImage(frame)
		#Search for Blue (white, "true") blobs in thresholded image
		mat = GetMat(imgBlueThresh)
		#Get the X and Y moments of the blobs
		moments = Moments(mat, 0)
		#Find the area of the blobs
		area = GetCentralMoment(moments, 0, 0)
		moment10 = GetSpatialMoment(moments, 1, 0)
		moment01 = GetSpatialMoment(moments, 0, 1)
		#Age position variables
		lastX = posX
		lastY = posY
		#if statement to only track blobs with an area bigger than 100,000
		if(area > 100000):
                   global posX
		   global posY
		   #Positions are calculated by dividing the moment by the area
		   #of the blob
		   posX = int(moment10/area)
		   posY = int(moment01/area)
		   #Print the position and area to the terminal
		   print 'x: '+str(posX)+' y: '+str(posY)+ ' area: '+str(area)
		   #If any position is not "false"(greater than zero), draw
		   #the trace line between them			
		   if(lastX > 0 and lastY > 0 and posX > 0 and posY >0):
			Line(imgScrible, (posX, posY), (lastX, lastY),
                        Scalar(0, 255, 255), 5)
		#Overlay the tracking image onto the videocapture image
	        Add(frame, imgScrible, frame)
		#Display the tracking image as well as the binary image
		ShowImage(thresh_window, imgBlueThresh)
		ShowImage(color_tracker_window, frame)
		#Wait for user input interupt
		c = WaitKey(10)
		if(c != -1):
		    break

	return;#End Main
####################################################################################
#Define the module name for main()
if __name__ == "__main__":
   main()
####################################################################################
#Run main continuously
while (1):
	main()
####################################################################################
