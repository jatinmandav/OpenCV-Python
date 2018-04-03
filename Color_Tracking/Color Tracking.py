# -----------------------------------------------------------------------------
#
# Color Tracking Using OpenCV
#
# Language - Python
# Modules - opencv, numpy, colorsys
#
# By - Jatin Kumar Mandav
#
# Website - https://jatinmandav.wordpress.com
#
# YouTube Channel - https://www.youtube.com/mandav
# GitHub - github.com/jatinmandav
# Twitter - @jatinmandav
#
# -----------------------------------------------------------------------------

import cv2
import numpy as np
import colorsys

# Video Input
video = cv2.VideoCapture(0)
toTrackCoor = [0, 0]
loc = [0, 0]
colorToTrack = []
hsvValue = []
threshold = 70

# Get Coordinates of Button Click and extract HSV color code at that Coordinate
def getCoordinates(event, x, y, flags, param):
    global toTrackCoor, frame, colorToTrack, hsvValue
    if event == cv2.EVENT_LBUTTONDOWN:
        toTrackCoor = [y, x]
        bgr = frame[toTrackCoor[0], toTrackCoor[1]]
        bgr = np.uint8([[[bgr[0], bgr[1], bgr[2]]]])
        hsvValue = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        print(hsvValue)
        

cv2.namedWindow("Color Tracking")
cv2.setMouseCallback("Color Tracking", getCoordinates)

# The Magic happens Here!
while True:
    _, frame = video.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Creating a range within which we have to track the color
    if not len(hsvValue) == 0:
        lower = np.array([hsvValue[0][0][0] - threshold, hsvValue[0][0][1] - threshold, hsvValue[0][0][2] - threshold])
        upper = np.array([hsvValue[0][0][0] + threshold, hsvValue[0][0][1] + threshold, hsvValue[0][0][2] + threshold])
    else:
        lower = np.array([0, 0, 0])
        upper = np.array([255, 255, 255])

    # Generating Mask and then Refining the masked Image
    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(mask,kernel,iterations = 1)
    
    res = cv2.bitwise_and(frame, frame, mask = mask) 
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (230, 230, 230), 3)

    cv2.imshow('Color Tracking', frame)
    cv2.imshow('Dilation',dilation)
    cv2.imshow('Only Color',res)
    
    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
