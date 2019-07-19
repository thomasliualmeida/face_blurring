import cv2
import numpy as np
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
            cv2.circle(mask,(x,y),5,(255,255,255),-1)
            cv2.circle(img,(x,y),5,(255,255,255),-1)
            vertices.append([x, y])

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

        cv2.circle(mask,(x,y),5,(255,255,255),-1)
        cv2.circle(img,(x,y),5,(255,255,255),-1)
        contours = np.array(vertices)
        pts =np.int32([contours])
        cv2.fillPoly(mask, pts =np.int32([contours]), color=(255,255,255))
        cv2.fillPoly(img, pts =np.int32([contours]), color=(255,255,255)) 
        vertices.clear()

##Next we have to bind this mouse callback function to OpenCV window. In the main loop, we should set a keyboard binding for key ‘m’ to toggle between rectangle and circle.

video_capture = cv2.VideoCapture('/home/veesion/Downloads/y2mate.com - radiohead_house_of_cards_scotch_mist_version_2yZBE5qLw8Y_144p.mp4')
width = int(video_capture.get(3))  # float
height = int(video_capture.get(4)) # float

total_frames = video_capture.get(7)
print('total frames: ' + str (total_frames))

vertices = [] #vertices should be placed here, otherwise its restarted in each iteraction
cv2.namedWindow('image')
cv2.namedWindow('mask')
cv2.setMouseCallback('image',draw_circle)

cv2.namedWindow('blurred') #display the result blurred frame
counter = 1 #gets frame position in the video

while True:
    ret, img = video_capture.read()
    mask = np.zeros((height,width,3), np.uint8)

    frameId = video_capture.get(1)
    print(str(frameId) + ' '+ str(counter))
    
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass
    clone = img.copy() #allows to restart the frame
    while True:
        cv2.imshow('image',img)
        cv2.imshow('mask',mask)
        blurred = img + mask
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
##            mask = cv2.imread('/media/veesion/GRE-INP/betas/Webcam-Face-Detect-master_2/face blurring final/images/mask_' + str(counter) + '.jpg')
            break
        if k == ord('f'):            
            counterNew = counter + skipRate
            if counterNew >= 0 and counterNew <= total_frames:
                print('perdeu playboi')
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
##            mask = cv2.imread('/media/veesion/GRE-INP/betas/Webcam-Face-Detect-master_2/face blurring final/images/mask_' + str(counter) + '.jpg')
            else:
                video_capture.set(1, counter -1)
            break 
            
        
    cv2.imwrite('/media/veesion/GRE-INP/betas/Webcam-Face-Detect-master_2/face blurring final/images/mask_' + str(counter) + '.jpg', mask)
    
cv2.destroyAllWindows()
