import cv2
import numpy as np

Kernel_size=15
low_threshold=40
high_threshold=80

rho=10
threshold=10
theta=np.pi/180
minLineLength=10
maxLineGap=1

frame = cv2.imread('frame0.jpg')
#Convert to Grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#Blur image to reduce noise. if Kernel_size is bigger the image will be more blurry
blurred = cv2.GaussianBlur(gray, (Kernel_size, Kernel_size), 0)

print blurred.shape

crop_img = blurred[200:240, 0:320]
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)

#Perform canny edge-detection.
#If a pixel gradient is higher than high_threshold is considered as an edge.
#if a pixel gradient is lower than low_threshold is is rejected , it is not an edge.
#Bigger high_threshold values will provoque to find less edges.
#Canny recommended ratio upper:lower  between 2:1 or 3:1
edged = cv2.Canny(crop_img, low_threshold, high_threshold)

cv2.imshow("cropped", edged)
cv2.waitKey(0)

lines = cv2.HoughLinesP(edged,rho,theta,threshold,minLineLength,maxLineGap)

cv2.imshow("cropped", lines)
cv2.waitKey(0)


cv2.imwrite("output.jpg", lines)



# get a frame out
# print(cv2.__version__)
# vidcap = cv2.VideoCapture('raw_video_feed.mp4')
# success,image = vidcap.read()
# count = 0
# success = True
# if success:
#     cv2.imwrite("frame%d.jpg" % count, image) 
