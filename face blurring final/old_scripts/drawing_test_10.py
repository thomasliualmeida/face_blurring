"""
Created on Mon Jul 15 14:32:15 2019

@author: Thomas Liu de Almeida
"""
"""
v8 Allows the user to make undo by steps
v9 Correct bug in which the mask was not updated with the undo.
    Actually, the polygone drawing was also being made on the img. Now it's done only on the mask,
    which is than added to the img to result in the blurred image
"""

import cv2
import numpy as np
import os
import ctypes  # An included library with Python install.


drawing = False # true if mouse is pressed
ix,iy = -1,-1

# mouse callback function
# borders made by a succesion of filled circles. Autofilling as a polygone in the end.
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode,updateUndo    

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(mask,(x,y),brushSize,(255,255,255),-1)
            vertices.append([x, y])

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(mask,(x,y),brushSize,(255,255,255),-1)
        updateUndo = True  #flag used on the 'undo by steps' functionality, to keep track of the changes in one frame. Updated for each time the left button of the mouse is realesed
        if len(vertices) > 0:
            contours = np.array(vertices)
            pts =np.int32([contours])
            cv2.fillPoly(mask, pts =np.int32([contours]), color=(255,255,255))
        vertices.clear()




def delete_files(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
             

path = os.getcwd() #get the project's folder

video_capture = cv2.VideoCapture(path + '/videos/merch_14_06_simu_cam_2_set_Benoit_Simu_8.mp4')
##video_capture = cv2.VideoCapture(path + '/videos/y2mate.com - radiohead_house_of_cards_scotch_mist_version_2yZBE5qLw8Y_144p.mp4')
width = int(video_capture.get(3))  # float
height = int(video_capture.get(4)) # float

total_frames = video_capture.get(7)

vertices = [] #vertices should be placed here, otherwise its restarted in each iteraction
##cv2.namedWindow('test', cv2.WINDOW_NORMAL)
cv2.namedWindow('blurred', cv2.WINDOW_NORMAL) #display the result blurred frame, sum of the mask and the original frame
cv2.setMouseCallback('blurred',draw_circle) #set the mouse callback funtion on the blurred image (we can see the changes in the mask over the original frame)
counter = 1 #gets frame position in the video

breakFlag = False #turns tru when 'p' is pressed, to exit he program

brushSize = 5
brushStep = height/150 

drawBarHeight = 0.01 #height of the progress bar on the bottom

#sets the speed of the forward/backward fonction
skipRate = int(total_frames/50)
updateUndo =False #when it turns to true, stores the last modificatrion in a list
while True:
    ret, img = video_capture.read()
    if os.path.isfile(path +'/images/mask_' + str(counter) + '.jpg'): #if the mask already exists, use it
        mask = cv2.imread(path +'/images/mask_' + str(counter) + '.jpg')
    else :
        mask = np.zeros((height,width,3), np.uint8) #if not, create an black image
    frameId = video_capture.get(1)
    print(str(frameId) + ' '+ str(counter))
    
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass
    undo=[] #list of modifications, used for the 'undo' fonctionallity
    currentCounter = counter
    while True:
        if updateUndo == True:
            undoElement = mask.copy() #if its not copied, the mask is also modified
            undo.append(undoElement)
        updateUndo = False
        
##        cv2.imshow('test',mask)
        videoProgress = counter/total_frames
        blurred = cv2.add(img , mask) #cv2.add() for adding images
        cv2.rectangle(blurred, (0,int(height*(1 - drawBarHeight))), (int(videoProgress*width),height), (0,0,255), -1) #creates the progress bar, length = progress
        cv2.imshow('blurred',blurred)
        k = cv2.waitKey(1) & 0xFF


        # if the 'r' key is pressed, performs the undo fonctionallity
        if k == ord('r'):
            if undo: #using the booleaness of a list
                mask = undo[-1] #-1 index gets the last element of a list               
                del undo[-1]
            else:
                mask = np.zeros((height,width,3), np.uint8) #
        #step forward, one frame        
        if k == ord('d'):
            if counter + 1 > 0 and counter + 1 <= total_frames:
                counter += 1
            video_capture.set(1, counter - 1)
            break
        #step backward, one frame 
        if k == ord('s'):
            counterNew = counter - 1
            if counterNew > 0 and counterNew <= total_frames:
                video_capture.set(1, counterNew -1)
                counter=counterNew
            else:
                video_capture.set(1, counter -1)
            break
        #step forward, multiple frames     
        if k == ord('f'):            
            counterNew = counter + skipRate
            if counterNew >= 0 and counterNew <= total_frames:
                video_capture.set(1, counterNew)
                counter=counterNew +1
            else:
                counter=total_frames
                video_capture.set(1, total_frames - 1)
            break
        #step backward, multiple frames 
        if k == ord('q'):
            counterNew = counter - skipRate
            if counterNew >= 0 and counterNew <= total_frames:
                video_capture.set(1, counterNew)
                counter=counterNew +1
            else:
                counter=1
                video_capture.set(1, 0)
            break

        #set brush's size
        if k == ord('+'):
            if brushSize + int(brushStep) < height/2:
                brushSize += int(brushStep)
        if k == ord('-'):
            if brushSize - int(brushStep) > 0:
                brushSize -= int(brushStep)
        
        #exits the program
        if k == ord('p'):
            breakFlag = True
            break
        
    cv2.imwrite(path + '/images/mask_' + str(currentCounter) + '.jpg', mask)
    #Asks for saving the work done. As the files are automatically saved, not saving the work erases the already saved files
    if breakFlag == True:
        answer = input("Do you want to save the work done? Y/N ")
        incorrect = True
        while incorrect:
            if answer not in ['Y', 'N'] :
                print("Please input the answer in the right format.")
                answer = input("Do you want to save the work done? Y/N ")
                incorrect = True 
            else:
                incorrect = False
        if answer == 'N' :
            delete_files(path + '/images')
            
        break
    
cv2.destroyAllWindows()
