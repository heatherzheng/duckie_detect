import rospy
import numpy as np
# Import ROS messages
from std_msgs.msg import String as String
from std_msgs.msg import Float64MultiArray as Float64MultiArray

class Obstacle_coord(object):

    def __init__(self):
        self.yolo_box = None
	self.box = rospy.Subscriber("bounding_box", Float64MultiArray, callback = self.call_back,queue_size=1)
        self.obstacle_coord = rospy.Publisher("obstacle_coord",String,queue_size=1)
	self.classes = None

    def call_back(self,data):
	print(data)
        self.yolo_box = data.data

    def convert(self):
        '''
        upperleft = [left,top]
        bottomright = [left+width,top+height]
        '''
        rate = rospy.Rate(15)

        while self.yolo_box is None:
            print(str(self.yolo_box))
	    rate.sleep()
        while not rospy.is_shutdown():
            print(str(self.yolo_box))
            upperleft = [self.yolo_box[0],self.yolo_box[1]]
            bottomright = [self.yolo_box[0]+self.yolo_box[2],self.yolo_box[1]+self.yolo_box[3]]
            center_x = self.yolo_box[0] + self.yolo_box[2]/2
            real_angle = round(-77.914994707 + 0.24613817 * center_x , 4)
            box_x = self.yolo_box[2]
            real_dist = round (1.0023585 - 0.02211239 * box_x +0.000132113398 * (box_x**2), 4)
            self.obstacle_coord.publish(str(real_angle)+" "+str(real_dist))

if __name__ == "__main__":
    try:
        rospy.init_node('Obstacle_coord', anonymous=True)
        obstacle_node = Obstacle_coord()
	obstacle_node.convert()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
