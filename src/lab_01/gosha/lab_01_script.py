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

# vidcap = cv2.VideoCapture('raw_video_feed.mp4')
# success,image = vidcap.read()
# count = 0
# success = True
# if success:
#     cv2.imwrite("frame%d.jpg" % count, image)


def draw_circle ():
    frame = cv2.imread('frame0.jpg')
    #Convert to Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Blur image to reduce noise. if Kernel_size is bigger the image will be more blurry
    blurred = cv2.GaussianBlur(gray, (Kernel_size, Kernel_size), 0)

    print blurred.shape

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

    # print edged.shape

    # TODO: find white 1 then 2 then average theur x pos
    # Black is 0 white is 1
    first_white = 0
    second_white = 0

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

    print average_white

    cv2.circle(frame,(average_white,210),20,(0,0,255),1)


    cv2.imshow("cropped", frame)
    cv2.waitKey(0)


    cv2.imwrite("output.jpg", edged)


draw_circle()



# get a frame out
# print(cv2.__version__)
# vidcap = cv2.VideoCapture('raw_video_feed.mp4')
# success,image = vidcap.read()
# count = 0
# success = True
# if success:
#     cv2.imwrite("frame%d.jpg" % count, image) 
