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
            velocity.angular.z = 0
            velocity.linear.x = 10
            self.publish.publish(velocity)
            print("forward")
            rospy.sleep(.7)
            velocity.angular.z = 10
            velocity.linear.x = 0
            self.publish.publish(velocity)
            print("turn")
            rospy.sleep(.5)
            velocity = Twist()
            velocity.angular.z = 0
            velocity.linear.x = 10
            self.publish.publish(velocity)
            print("forward")
            rospy.sleep(.7)
            self.drifted = True

    # determineVelocity function calculate the velocity for the robot based
    # on the position of the line in the image.   
    def determineVelocity(self, image):
        
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayImage,(9, 9), 0)
        grayInverseImage = blurred
        bw = cv2.threshold(grayInverseImage, 147, 255, cv2.THRESH_BINARY)[1]

        h, w = bw.shape[0:2]  # gets dimensions of image
        # cv2.imshow("cropped", bw)
        # cv2.waitKey(3)
        imageCentre = 1222-20

        turn_sum = 0 
        for x in range(w-1):
            turn_sum += bw[h-200, x]
        # print(turn_sum)
        # finds where the line is on the bottom of the image
        left_x = -34  # random numbers that is supposed to be repalce with one when line is found
        right_x = -34
        f_left_x = -34 
        f_right_x = -34
        
        for x in range(w-int(w/2)-1):
            if (bw[h - 5*2, x+int(w/2)] > 0):
                left_x = x+int(w/2)
                break #aproach from left toright of frame will always happen later ahead in bots perspective 
            if (bw[h - 5*5, x+int(w/2)] > 0):
                f_left_x = x+int(w/2)

        for x in range(w-1):
            if (bw[h - 5*2, w-x-1] > 0):
                right_x = w-x
            if (bw[h - 5*5, w-x-1] > 0):
                f_right_x = w-x
                break #aproach from right to left of frame will always happen later ahead in bots perspective 

        lineCentre = int(left_x+right_x)/2
        f_lineCentre = int(f_left_x+f_right_x)/2

        # print(f_lineCentre)
        # print(lineCentre,"\n--------------------")
        # print(left_x , "left aaaaaaaaaaand Right" , right_x)
        lineBufferZone = 12
        straightZoneLeftBoundary = imageCentre - lineBufferZone
        straightZoneRightBoundary = imageCentre + lineBufferZone
        distance_error = abs(imageCentre - lineCentre)/imageCentre
        turn_multiplier = (1-distance_error)
        print
        velocity = Twist()
         # tokyo drift to outside in begining
        # if turn_sum > 35000:
        #     print("hard tuning ---------------")
        #     velocity.linear.x = 0
        #     velocity.angular.z = 10    
        if lineCentre < 0 or 2 < abs(f_lineCentre-lineCentre) < 5 :
            # print("cant see shit so go stright")
            velocity.linear.x = 1
        # goes through different options of turning
        elif lineCentre < straightZoneLeftBoundary : #or abs(f_lineCentre-lineCentre)<2
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
