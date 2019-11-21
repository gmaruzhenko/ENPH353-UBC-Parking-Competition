#!/usr/bin/env python
from __future__ import print_function

import roslib
# roslib.load_manifest('enph353_ros_lab')
import sys
import time
import glob
import numpy as np
import rospy
import cv2
import csv
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
        self.rotate = 0
        self.direction = True


    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        #TODO FIND CORRECT LICENCE PLATE
        # csv_data = np.genfromtxt('/home/gosha/Code/comp_ws/src/2019F_competition_student/enph353/enph353_gazebo/scripts/plates.csv',delimiter='\n')
        # print(csv_data)
        with open('/home/gosha/Code/comp_ws/src/2019F_competition_student/enph353/enph353_gazebo/scripts/plates.csv', 'rb') as csvfile:
            data = list(csv.reader(csvfile))
        label = '/home/gosha/Code/comp_ws/dataset/'+str(time.time())+'@'+data[1][0]+'.png'
        # print(data[1])
        cv2.imwrite(label,cv_image)
        # rospy.sleep(0.05)
        #rotate a hair and repeat 
        velocity = Twist()
        #roatate in a deiretion within a certain angle
        if self.direction:
            velocity.angular.z = -0.1
        else:
            velocity.angular.z = 0.1
        velocity.linear.x = 0
        self.publish.publish(velocity)
        self.rotate += 1
        
        rospy.sleep(0.01)

        velocity.angular.z = 0
        self.publish.publish(velocity)

        rospy.sleep(0.1)



    # determineVelocity function calculate the velocity for the robot based
    # on the position of the line in the image.

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
