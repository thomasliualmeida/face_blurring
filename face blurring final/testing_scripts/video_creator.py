import cv2
import numpy as np
import glob
import os
import re

'''
From https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
'''
path = os.getcwd() #get the project's folder
 
img_array = []
size = (4,3)

##filelist = glob.glob(os.path.join(path, '/blurred/*.jpg'))
filelist = glob.glob(path + '/blurred/*.jpg')

##for filename in filelist:
##    print(re.search(path + '/blurred/(.*).jpg', filename).group(1))


##filelist = sorted(filelist)

##result = re.search(path + '/blurred/(.*).jpg', filename)


filelist.sort(key = lambda filename: int(re.search(path + '/blurred/(.*).jpg', filename).group(1)))
print(filelist)
for filename in filelist:
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
##    print(filename)
 
 
out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 25, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()


