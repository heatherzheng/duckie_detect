import rospy

# Import OpenCV and numpy
import cv2
import numpy as np

# Import CV Bridge for transforming between ROS image messages and OpenCV images
from cv_bridge import CvBridge

# Import ROS messages
from std_msgs.msg import String as String
from sensor_msgs.msg import Image, CompressedImage


class DuckDetector(object):
    
    def __init__(self):
        # TODO enter the names of the Duckiebot's camera topic and the LED color pattern changing topic
        camera_topic_name = '/duckiebot1/camera_node/image/compressed'
        lights_topic_name = '/duckiebot1/coordinator_node/change_color_pattern'
        # ENDTODO
        self.bridge = CvBridge()
        self.image = None
        self.image_sub = rospy.Subscriber(camera_topic_name, CompressedImage,
                                          callback=self.image_callback)
                                          self.mask_image_pub = rospy.Publisher("yellow_mask_image/compressed", CompressedImage,
                                                                                queue_size=1)
                                          
                                          # TODO create the publisher that publishes to the LED color pattern changing topic
        self.lights_pub = rospy.Publisher(lights_topic_name, String, queue_size=10)
    # ENDTODO
    
    def image_callback(self, image_msg):
        self.image = self.bridge.compressed_imgmsg_to_cv2(image_msg, "bgr8")
    
    def run(self):
        rate = rospy.Rate(15)
        
        # Wait until an image is received
        while self.image is None:
            rate.sleep()
        
        # Keep looping until node is shut down
        while not rospy.is_shutdown():
            hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            # Note that in OpenCV, hue is in the range [0, 179]
            # Saturation and value are both in the range [0, 255]
            hue = hsv_image[:,:,0]
            
            # TODO set the lower and upper limits for the hue mask, to just get yellow pixels
            hue_low = 20
            hue_high = 40
            # ENDTODO
            hue_is_yellow = np.logical_and(hue > hue_low, hue < hue_high)
            
            # TODO Create the mask
            #      Use np.logical_and to get the pixels that have yellow hue, and
            #      also have saturation and value above some thresholds that you set
            saturation = hsv_image[:,:,1]
            value = hsv_image[:,:,2]
            mask = np.logical_and(hue_is_yellow,saturation>100,value>100)
            
            # ENDTODO
            
            # TODO Count the number of yellow pixels, which will be printed to console
            #n_pixels = np.sum(mask)
            # ENDTODO
            #print("I see %d yellow pixels!" % n_pixels)
            # Create a BGR mask image and publish it to show results
            up = 0
            state = True
            down  = 0
            left = 0
            right = 0
            '''
                for i in range(mask):
                for j in range(i):
                if(mask[i][j]==1 && state):
                up = i
                down = i
                left = j
                right = j
                state = False
                elif(mask[i][j]==1):
                if(i>down):
                down  = i
                if(j<left):
                left = j
                if(j>right):
                right = j
                '''
            mask_image = np.zeros(hsv_image.shape)
            mask_image[:,:,2] = 255
            mask_image[mask,1] = 255
            
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])
            mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
            blob = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for j, contour in enumerate(contours):
                if(len(contour)<20):
                    continue
                bbox = cv2.boundingRect(contour)
                # Create a mask for this contour
                contour_mask = np.zeros_like(mask)
                cv2.drawContours(contour_mask, contours, j, 255, -1)
                
                # Extract and save the area of the contour
                region = blob.copy()[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2]]
                region_mask = contour_mask[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2]]
                region_masked = cv2.bitwise_and(region, region, mask=region_mask)
                
                # Extract the pixels belonging to this contour
                result = cv2.bitwise_and(blob, blob, mask=contour_mask)
                # And draw a bounding box
                top_left, bottom_right = (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3])
            cv2.rectangle(mask_image, top_left, bottom_right, (255, 255, 255), 2)
            print(top_left,bottom_right)
            print("done")
            
            #print(up,down,left,right)
            
            # TODO use CV Bridge to convert the mask image to a CompressedImage message, and then publish it
            cv_image = self.bridge.cv2_to_compressed_imgmsg(mask_image)
            self.mask_image_pub.publish(cv_image)
            # ENDTODO
            
                rate.sleep()



if __name__ == "__main__":
    rospy.init_node("duck_detector")
    detector = DuckDetector()
    detector.run()

