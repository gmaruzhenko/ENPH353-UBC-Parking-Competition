#!/usr/bin/env python
# /R1/cmd_vel
# /R1/pi_camera/image_raw

# control robot movement
# Copied code for node from http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython

from __future__ import print_function

import roslib
# roslib.load_manifest('enph353_ros_lab')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist


class image_converter:

    def __init__(self):
        # we want to subscribe to the image that is published automatically by the camera
        # then we want to publish the velocity which is automatically heard by the robot
        # self.image_pub = rospy.Publisher("image_topic_2", Image)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/R1/pi_camera/image_raw", Image, self.callback)

        self.publish = rospy.Publisher("/R1/cmd_vel", Twist, queue_size=1)
        self.drifted = False

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        # Gets the velocity message from the determineVelocity function
        velocity = self.determineVelocity(cv_image)
        self.publish.publish(velocity)
        if not self.drifted:
            velocity = Twist()
            velocity.linear.x = 10
            self.publish.publish(velocity)
            rospy.sleep(.8)
            velocity.angular.z = 10
            self.publish.publish(velocity)
            rospy.sleep(.5)
            self.drifted = True

    # determineVelocity function calculate the velocity for the robot based
    # on the position of the line in the image.   
    def determineVelocity(self, image):
        
        # # Crop the image
        # crop_img = image[60:120, 0:160]
        # # Convert to grayscale
        # gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        # # Gaussian blur
        # blur = cv2.GaussianBlur(gray,(5,5),0)
        # # Color thresholding
        # ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
        # # Find the contours of the frame

        # contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # cv2.imshow("cropped", contours)
        # cv2.waitKey(3)
        # print(hierarchy)
        
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayImage,(9, 9), 0)
        grayInverseImage = blurred
        bw = cv2.threshold(grayInverseImage, 147, 255, cv2.THRESH_BINARY)[1]

        h, w = bw.shape[0:2]  # gets dimensions of image
        # cv2.imshow("cropped", bw)
        # cv2.waitKey(3)
        imageCentre = 1200#1222

        turn_sum = 0 
        for x in range(w-1):
            turn_sum += bw[h-200, x]
        # print(turn_sum)
        # finds where the line is on the bottom of the image
        left_x = -34  # random numbers that is supposed to be repalce with one when line is found
        right_x = -34
        for x in range(w-int(w/2)-1):
            if (bw[h - 5*3, x+int(w/2)] > 0):
                left_x = x+int(w/2)
                break

        for x in range(w-1):
            if (bw[h - 5*3, w-x-1] > 0):
                right_x = w-x
                break

        lineCentre = int(left_x+right_x)/2
        # print(left_x , "left aaaaaaaaaaand Right" , right_x)
        lineBufferZone = 12
        straightZoneLeftBoundary = imageCentre - lineBufferZone
        straightZoneRightBoundary = imageCentre + lineBufferZone
        distance_error = abs(imageCentre - lineCentre)/imageCentre
        turn_multiplier = (1-distance_error)
        
        velocity = Twist()
         # tokyo drift to outside in begining
        # if turn_sum > 35000:
        #     print("hard tuning ---------------")
        #     velocity.linear.x = 0
        #     velocity.angular.z = 10    
        if lineCentre < 0:
            # print("cant see shit so go stright")
            velocity.linear.x = 1
        # goes through different options of turning
        elif lineCentre < straightZoneLeftBoundary:
            # turn right Cop
            # print("turning right")
            velocity.linear.x = 0
            velocity.angular.z = 0.1*turn_multiplier
        elif lineCentre > straightZoneRightBoundary:
            # turn left
            # print("turning Left")
            velocity.linear.x = 0
            velocity.angular.z = -0.1*turn_multiplier
        else:
            # go straight
            # print("straight")
            velocity.linear.x = 0.3
            velocity.angular.z = 0
        return velocity


# the main function is what is run
# calls on the image_converter class and initializes a node
def main(args):
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()  # spin() keeps python from exiting until the node is stopped
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
