# Lab 1: Use the lower 100 pixels of a video to determine the location of a line. 
# Steps:
# 1. Extract frames from a video 
# 2. Threshold/transform image
# 3. Find location of object (in pixels) and store in a matrix
# 4. Output dot and matrix to screen. 
#from __future__ import division

import cv2
import numpy as np 
import cython

height = 220

# Opens the Video file
cap= cv2.VideoCapture('raw_video_feed.mp4')

def location(height, image):
    # set the variable extension types
    
    # grab the image dimensions
    h = image.shape[0]
    w = image.shape[1]

    leftswitch, rightswitch = None, None
    
    # loop over the image
    for x in range(0, w):
        if leftswitch == None and image[height, x] == 255:
            leftswitch = x
        elif leftswitch != None and rightswitch == None and image[height,x] == 0:
            rightswitch = x 
    
    if leftswitch == None:
        leftswitch = 0
    if rightswitch == None:
        rightswitch = w
            
    # return the thresholded image
    return (leftswitch + rightswitch)/2


i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur the image to reduce noise
    img_blur = cv2.medianBlur(gray, 25)
    
    # attempt at line detection
    # canny = cv2.Canny(img_blur, 50, 100)
    # lines = cv2.HoughLinesP(canny,cv2.HOUGH_PROBABILISTIC, np.pi/180, 5, minLineLength,maxLineGap)
    # for x in range(0, len(lines)):
    #     for x1,y1,x2,y2 in lines[x]:
    #         #cv2.line(inputImage,(x1,y1),(x2,y2),(0,128,0),2, cv2.LINE_AA)
    #         pts = np.array([[x1, y1 ], [x2 , y2]], np.int32)
    #         cv2.polylines(frame, [pts], True, (0,255,0))

    # doing threshold instead.
    ret, thr = cv2.threshold(img_blur, 120, 500, cv2.THRESH_BINARY_INV)
    done = cv2.circle(frame, (location(height, thr), height), 10, (0, 0, 255), -1)

    cv2.imshow('Frame',frame)
    cv2.waitKey(0)
    #cv2.imwrite('output/frame'+str(i)+'.jpg', done)

    i+=1


 
cap.release()
cv2.destroyAllWindows()