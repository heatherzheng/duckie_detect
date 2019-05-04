import rospy
import numpy as np
# Import ROS messages
from std_msgs.msg import String as String
from std_msgs.msg import Float64MultiArray as Float64MultiArray

class Obstacle_coord(object):

    def __init__(self):
        self.yolo_box = rospy.Subscriber("bounding_box", Float64MultiArray, queue_size=1)
        self.obstacle_coord = rospy.Publisher("obstacle_coord",String,queue_size=1)
	    self.classes = None

    def convert(self):
        '''
        upperleft = [left,top]
        bottomright = [left+width,top+height]
        '''
        upperleft = [self.yolo_box[0],self.yolo_box[1]]
        bottomright = [self.yolo_box[0]+self.yolo_box[2],self.yolo_box[1]+self.yolo_box[3]]
        center_x = (upperleft[0]+bottomright[0])/2
        real_angle = round(-77.91499470711372 + 0.24613817086717288 * center_x , 2)
        #real_angle = round(-70.42606156071501 + 0.21226782927377597 * center_x , 2)
        box_x = (upperleft[0] - bottomright[0])/2
        real_dist = round (0.7187183182533904 - 0.007269440794712034 * box_x , 2)
        real_dist_curve  = round(1.0023585031960698 - 0.022112391488776546 * box_x
                            + 0.00013211339801794553 * box_x **2,2)
        #real_dist = round (49.39505723660218 - 0.36358177568161004 * box_x , 2)
        self.obstacle_coord.publish(str(real_angle)+" "+str(real_dist))

if __name__ == "__main__":
    try:
        rospy.init_node('Obstacle_coord', anonymous=True)
        obstacle_node = Obstacle_coord()
	    obstacle_node.convert()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
