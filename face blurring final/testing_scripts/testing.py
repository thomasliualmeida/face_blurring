import cv2
import numpy as np
import os
import ctypes  # An included library with Python install. 

def draw_progress_bar(img, width, height, videoProgress):
    cv2.rectangle(mask, (0,int(height*(1 - drawBarHeight))), (int(progress*width),height), (255,0,0), -1)
    
cv2.namedWindow('teste', cv2.WINDOW_NORMAL)
  

path = os.getcwd()

video_capture = cv2.VideoCapture(path + '/videos/merch_14_06_simu_cam_2_set_Benoit_Simu_8.mp4')
width = int(video_capture.get(3))  # float
height = int(video_capture.get(4)) # float

mask = np.zeros((height,width,3), np.uint8)

videoProgress = 0.8
drawBarHeight = 0.01 # height inproportion to the image's height

##print(width, height)
##cv2.imshow('blurred',mask)

cv2.imshow('teste',mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
