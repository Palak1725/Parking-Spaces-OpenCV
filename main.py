import cv2
import pickle
import cvzone
import numpy as np

#Video feed
cap = cv2.VideoCapture('carPark.mp4') #reading the video of parking lot [dynamic image]

with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
width, height = 107, 48

def checkParkingSpace(imgProcess):
    spaceCounter = 0
    for pos in posList:
        x,y = pos
        imgCrop = imgProcess[y:y+height, x:x+width] #crop the image to the size of the parking space
        #cv2.imshow(str(x*y), imgCrop) #show the cropped image of the parking space
        count = cv2.countNonZero(imgCrop)
        if count < 970:
            color = (0,255,0) #green
            thickness = 5
            spaceCounter+=1
        else:
            color = (0,0,255) #red
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y+height-3), scale = 1, thickness = 2, offset = 0, colorR = color) #put the count of non-zero pixels on the image
    cvzone.putTextRect(img, f'Free:{spaceCounter}/{len(posList)}', (100, 50), scale = 3, thickness = 5, offset = 20, colorR = (0,200, 0)) #put the count of non-zero pixels on the image

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT): #if the current frame == total frames in video or video has reached the end--> reset to the beginning
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) #reset to the beginning of the video
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert the image to grayscale
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16) #adaptive thresholding to get the binary image
    imgMedian = cv2.medianBlur(imgThreshold, 5) #median blur to remove lil bits of noise
    kernel = np.ones((3,3), np.uint8) #kernel for dilation
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1) #dilate the image to fill the gaps


    checkParkingSpace(imgDilate) #check the parking spaces in the image
    #for pos in posList:
        
    cv2.imshow("Image", img)
    #cv2.imshow("ImageBlur", imgBlur)
    #cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(10)