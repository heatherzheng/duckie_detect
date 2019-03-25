import cv2
import os

image_folder = 'particlefilter'
video_name = 'video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images.sort()
print(images)
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 1, (width,height))

for i in range(135):
    video.write(cv2.imread(os.path.join(image_folder, str(i)+".png")))

cv2.destroyAllWindows()
video.release()
