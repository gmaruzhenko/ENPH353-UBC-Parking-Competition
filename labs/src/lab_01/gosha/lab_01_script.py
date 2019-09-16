import cv2
import numpy as np
import time

Kernel_size=15
low_threshold=40
high_threshold=80

#Source of video
vidcap = cv2.VideoCapture('raw_video_feed.mp4')

#get first frame loaded up
success,image = vidcap.read()
# frame count itterator setup
count = 0
success = True
while success:
    #Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Blur image to reduce noise. if Kernel_size is bigger the image will be more blurry
    blurred = cv2.GaussianBlur(gray, (Kernel_size, Kernel_size), 0)

    #debug to find size of image
    # print blurred.shape

    # crop down to last few slices (actually not needed)
    crop_img = blurred[200:240, 0:320]

    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)

    #Perform canny edge-detection.
    #If a pixel gradient is higher than high_threshold is considered as an edge.
    #if a pixel gradient is lower than low_threshold is is rejected , it is not an edge.
    #Bigger high_threshold values will provoque to find less edges.
    #Canny recommended ratio upper:lower  between 2:1 or 3:1
    edged = cv2.Canny(crop_img, low_threshold, high_threshold)

    # cv2.imshow("cropped", edged)
    # cv2.waitKey(0)

    # Note Black is 0 white is 1
    # Find first and second occurance of contour plot on second to
    # last row of pixel (approximation of real path)
    first_white = 0
    second_white = 0

    #due to image size
    index_max = 320
    index = 0

    while index<index_max:

        if edged[39,index] > 0:
            if first_white == 0:
                first_white = index
            else:
                second_white = index
        

        index+=1

    average_white = int((first_white+second_white)/2)

    # print average_white

    # Now draw circle showing the center location of our contour line
    cv2.circle(image,(average_white,210),20,(0,0,255),1)

    # run the slideshow at a min wait of 1 ms
    cv2.imshow("cropped", image)
    cv2.waitKey(1)

    #reset image for next frame 
    success,image = vidcap.read()

    count += 1


