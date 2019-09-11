import cv2
print(cv2.__version__)
vidcap = cv2.VideoCapture('raw_video_feed.mp4')
success,image = vidcap.read()
count = 0
success = True
if success:
    cv2.imwrite("frame%d.jpg" % count, image) 
