import cv2
import numpy as np
import glob
import os

'''
https://www.geeksforgeeks.org/rename-multiple-files-using-python/
https://stackoverflow.com/questions/7208861/replace-characters-not-working-in-python
https://stackoverflow.com/questions/16148951/python-looping-over-files-order
'''

path = os.getcwd() #get the project's folder
 
filelist = glob.glob(os.path.join(path, '/blurred/*.jpg'))
filelist = glob.glob(path + '/blurred/*.jpg')
for filename in filelist:
    newFileName = filename
    newFileName = newFileName.replace("blurred_","")
    os.rename(filename, newFileName)    
