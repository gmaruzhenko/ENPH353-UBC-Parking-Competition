from __future__ import print_function

import roslib
# roslib.load_manifest('enph353_ros_lab')
import sys
import glob
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


    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        #TODO FIND CORRECT LICENCE PLATE
        print(glob.glob("home/"))



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
