import cv2
import numpy as np
import os
import ctypes  # An included library with Python install.   

##First attempt on drawing filled figures
##
drawing = False # true if mouse is pressed
ix,iy = -1,-1

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode    

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(mask,(x,y),brushSize,(255,255,255),-1)
            cv2.circle(img,(x,y),brushSize,(255,255,255),-1)
            vertices.append([x, y])

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(mask,(x,y),brushSize,(255,255,255),-1)
        cv2.circle(img,(x,y),brushSize,(255,255,255),-1)
        if len(vertices) > 0:
            contours = np.array(vertices)
            pts =np.int32([contours])
            cv2.fillPoly(mask, pts =np.int32([contours]), color=(255,255,255))
            cv2.fillPoly(img, pts =np.int32([contours]), color=(255,255,255)) 
        vertices.clear()

##Next we have to bind this mouse callback function to OpenCV window. In the main loop, we should set a keyboard binding for key ‘m’ to toggle between rectangle and circle.


def delete_files(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
             

path = os.getcwd()

video_capture = cv2.VideoCapture(path + '/videos/merch_14_06_simu_cam_2_set_Benoit_Simu_8.mp4')
##video_capture = cv2.VideoCapture(path + '/videos/y2mate.com - radiohead_house_of_cards_scotch_mist_version_2yZBE5qLw8Y_144p.mp4')
width = int(video_capture.get(3))  # float
height = int(video_capture.get(4)) # float

total_frames = video_capture.get(7)

vertices = [] #vertices should be placed here, otherwise its restarted in each iteraction
##cv2.namedWindow('image')
##cv2.namedWindow('mask')
cv2.namedWindow('blurred', cv2.WINDOW_NORMAL) #display the result blurred frame
cv2.setMouseCallback('blurred',draw_circle)
counter = 1 #gets frame position in the video

breakFlag = False


brushSize = 5
brushStep = height/150

drawBarHeight = 0.01

while True:
    ret, img = video_capture.read()
    if os.path.isfile(path +'/images/mask_' + str(counter) + '.jpg'):
        mask = cv2.imread(path +'/images/mask_' + str(counter) + '.jpg')
##        img=cv2.add(img , mask)
    else :
        mask = np.zeros((height,width,3), np.uint8)
    frameId = video_capture.get(1)
    print(str(frameId) + ' '+ str(counter))
    
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass
    clone = img.copy() #allows to restart the frame
    currentCounter = counter
    while True:
##        cv2.imshow('image',img)
##        cv2.imshow('mask',mask)
        videoProgress = counter/total_frames
        blurred = cv2.add(img , mask) #cv2.add() for adding images
        cv2.rectangle(blurred, (0,int(height*(1 - drawBarHeight))), (int(videoProgress*width),height), (0,0,255), -1)
        cv2.imshow('blurred',blurred)
        k = cv2.waitKey(1) & 0xFF

        #defines the speed of the forward/backward fonction
        skipRate = int(total_frames/50)

        # if the 'r' key is pressed, reset the cropping region
        if k == ord('r'):
            img = clone.copy()
            mask = np.zeros((height,width,3), np.uint8)
        if k == ord('d'):
            if counter + 1 > 0 and counter + 1 <= total_frames:
                counter += 1
            video_capture.set(1, counter - 1)
            break        
        if k == ord('s'):
            counterNew = counter - 1
            if counterNew > 0 and counterNew <= total_frames:
                video_capture.set(1, counterNew -1)
                counter=counterNew
            else:
                video_capture.set(1, counter -1)
            break
        if k == ord('f'):            
            counterNew = counter + skipRate
            if counterNew >= 0 and counterNew <= total_frames:
                video_capture.set(1, counterNew)
                counter=counterNew +1
            else:
                video_capture.set(1, counter -1)
            break        
        if k == ord('q'):
            counterNew = counter - skipRate
            if counterNew >= 0 and counterNew <= total_frames:
                video_capture.set(1, counterNew)
                counter=counterNew +1
            else:
                video_capture.set(1, counter -1)
            break
        
        if k == ord('+'):
            if brushSize + int(brushStep) < height/2:
                brushSize += int(brushStep)
        if k == ord('-'):
            if brushSize - int(brushStep) > 0:
                brushSize -= int(brushStep)
        
        
        if k == ord('p'):
            breakFlag = True
            break
        
    cv2.imwrite(path + '/images/mask_' + str(currentCounter) + '.jpg', mask)
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
