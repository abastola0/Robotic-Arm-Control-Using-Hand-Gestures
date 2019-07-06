import argparse
import cv2
import numpy as np
import time
from pynput.mouse import Button, Controller
import wx
import pandas as pd

# lowerBound = np.array([ 63, 245,  74])
# upperBound =np.array([ 93 ,265 ,189])
# set lower and upperbounds by corping roi from image
lowerBound = None
upperBound =None

def set_threshold(ar1, ar2):
	print("the HSV is set for the range of \n{} \n{} ".format(ar1,ar2))
	global lowerBound
	lowerBound = ar1
	global upperBound
	upperBound = ar2
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
x_start, y_start, x_end, y_end = 0, 0, 0, 0
cropping = False
getROI = False
refPt = []

# construct the argument parser and parse the arguments
##ap = argparse.ArgumentParser()
##ap.add_argument("-i", "--image", required=True, help="Path to the image")
##args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
cap= cv2.VideoCapture(0)
for i in range(5):
	time.sleep(0.2)
	_,_ = cap.read()
_,image = cap.read()
clone = image.copy()


def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global x_start, y_start, x_end, y_end, cropping, getROI

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		x_start, y_start, x_end, y_end = x, y, x, y
		cropping = True

	elif event == cv2.EVENT_MOUSEMOVE:
		if cropping == True:
			x_end, y_end = x, y

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		x_end, y_end = x, y
		cropping = False
		getROI = True


cv2.namedWindow("image")

cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:

	i = image.copy()

	if not cropping and not getROI:
		cv2.imshow("image", image)

	elif cropping and not getROI:
		cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
		cv2.imshow("image", i)

	elif not cropping and getROI:
		cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
		cv2.imshow("image", image)

	key = cv2.waitKey(1) & 0xFF

	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
		getROI = False

	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

# if there are two reference points, then crop the region of interest
# from teh image and display it
refPt = [(x_start, y_start), (x_end, y_end)]
if len(refPt) == 2:

	roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
	try:
		cv2.imshow("ROI", roi)
	except:
		print('you didnt corp the roi properly! \n please restart the program!! ')
		exit()
	hsvRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
	# print('min H = {}, min S = {}, min V = {}; max H = {}, max S = {}, max V = {}'.format(hsvRoi[:,:,0].min(), hsvRoi[:,:,1].min(), hsvRoi[:,:,2].min(), hsvRoi[:,:,0].max(), hsvRoi[:,:,1].max(), hsvRoi[:,:,2].max()))

	lower = np.array([hsvRoi[:,:,0].min()-16, hsvRoi[:,:,1].min()-16, hsvRoi[:,:,2].min()-16])
	upper = np.array([hsvRoi[:,:,0].max()+16, hsvRoi[:,:,1].max()+16, hsvRoi[:,:,2].max()+16])
	set_threshold(lower,upper)


	image_to_thresh = clone
	hsv = cv2.cvtColor(image_to_thresh, cv2.COLOR_BGR2HSV)

	kernel = np.ones((3,3),np.uint8)
	# for red color we need to masks.
	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

	cv2.imshow("Mask", mask)
	print("is the ROI properly distinguished??\nif yes press 'c' else press'q'")
	while 1:
		if cv2.waitKey(5) & 0XFF == ord('c'):
			break
		elif cv2.waitKey(5) & 0XFF == ord('q'):
			exit()

cv2.destroyAllWindows()

mouse=Controller() # create a controller that controls mouse movements and events
t_end = time.time() + 25
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()

cam= cv2.VideoCapture(0)

kernelOpen=np.ones((4,4))
kernelClose=np.ones((20,20))
pinchFlag=0


kernel = np.ones((5,5),np.uint8)
# set the resolution
resx = 340
resy = 220
(camx,camy)=(resx,resy)
a = 1.5

while True:
	ret, img=cam.read()
	# img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
	img=cv2.resize(img,(resx,resy))
	# img = cv2.GaussianBlur(img,(5,5),0)

	#convert BGR to HSV
	imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	# create the Mask
	mask=cv2.inRange(imgHSV,lowerBound,upperBound)
	#morphology
	maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
	maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
	dilation = cv2.dilate(maskClose,kernel,iterations = 1)
	_,conts,h=cv2.findContours(dilation.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	for contours in conts:
		x1,y1,w1,h1=cv2.boundingRect(contours)
		cv2.rectangle(dilation, (x1,y1),(x1+w1,y1+h1), (255, 255, 255), -1)

		# cv2.fillPoly(dilation, pts =[(x1,y1),(x1+w1,y1+h1)], color=(255,255,255))
	maskFinal=dilation
	cv2.imshow('final mask',maskFinal)
	_,conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	if len(conts) == 0:
		mouse.release(Button.left)

	if(len(conts)==2):
		if(pinchFlag==1):
			pinchFlag=0
			mouse.release(Button.left)
		x1,y1,w1,h1=cv2.boundingRect(conts[0])
		x2,y2,w2,h2=cv2.boundingRect(conts[1])

		cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
		cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
		cx1=int(x1+w1/2)
		cy1=int(y1+h1/2)
		cx2=int(x2+w2/2)
		cy2=int(y2+h2/2)
		cx=int((cx1+cx2)/2)
		cy=int((cy1+cy2)/2)
		cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
		cv2.circle(img, (cx,cy),2,(0,0,255),2)

		mouseLoc=((sx-(cx*sx/camx)),(cy*sy/camy))
		# print(mouseLoc)
		mouse.position=mouseLoc
		# while mouse.position!=mouseLoc:
		#     pass

	elif(len(conts)==1):
		x,y,w,h=cv2.boundingRect(conts[0])

		if(pinchFlag==0):
			pinchFlag=1
			mouse.press(Button.left)
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		cx=int(x+w/2)
		cy=int(y+h/2)
		cv2.circle(img,(cx,cy),int((w+h)/4),(0,0,255),2)
		mouseLoc=(sx-(cx*sx/camx), cy*sy/camy)
		mouse.position=mouseLoc

	elif(len(conts)==4):
		if(pinchFlag==1):
			pinchFlag=0
			mouse.release(Button.left)
		x1,y1,w1,h1=cv2.boundingRect(conts[0])
		x2,y2,w2,h2=cv2.boundingRect(conts[1])
		x3,y3,w3,h3=cv2.boundingRect(conts[2])
		x4,y4,w4,h4=cv2.boundingRect(conts[3])

		cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
		cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
		cv2.rectangle(img,(x3,y3),(x3+w3,y3+h3),(255,0,0),2)
		cv2.rectangle(img,(x4,y4),(x4+w4,y4+h4),(255,0,0),2)

		cx1=int(x1+w1/2)
		cy1=int(y1+h1/2)
		cx2=int(x2+w2/2)
		cy2=int(y2+h2/2)

		cx3=int(x3+w3/2)
		cy3=int(y3+h3/2)
		cx4=int(x4+w4/2)
		cy4=int(y4+h4/2)

		cx12=int((cx1+cx2)/2)
		cy12=int((cy1+cy2)/4)
		cx34=int((cx3+cx4)/2)
		cy34=int((cy3+cy4)/2)

		cx=int((cx12+cy12)/2)
		cy=int((cx34+cy34)/2)

		cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
		cv2.line(img, (cx3,cy3),(cx4,cy4),(255,0,0),2)
		cv2.circle(img, (cx,cy),2,(0,0,255),2)

		mouseLoc=((sx-(cx*sx/camx)),(cy*sy/camy))
		mouse.position=mouseLoc
	cv2.imshow("cam",img)
	if cv2.waitKey(1) & 0XFF == ord('g'):
	# if (cv2.waitKey(1) & 0XFF == ord('g')) or (time.time() > t_end):
		cv2.destroyAllWindows()
		cam.release()
		break
