import cv2
import pickle #package used for saving teh positions of parking spaces and bring it to main code

#img = cv2.imread('carParkImg.png') #reading the image of parking lot [static image]

width, height = 107, 48 #width and height of the parking space determined from below comment

posList = [] #list to store the positions of parking spaces

#carParkPos not overwritten but changes made to the same
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f) #load the positions of parking spaces from the file
except:
    posList = [] 

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN: #if left mouse button is clicked
        posList.append((x,y)) #append the position of the parking space to the list
    if events == cv2.EVENT_RBUTTONDOWN: #if right mouse button is clicked
        for i, pos in enumerate(posList):
            if pos[0] < x < pos[0] + width and pos[1] < y < pos[1] + height: #if the right mouse button is clicked on a parking space
                posList.pop(i) #remove the position of the parking space from the list

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f) #save the positions of parking spaces to the file

while True:
    img = cv2.imread('carParkImg.png') #reading the image of parking lot [earlier it was a static image so anything drawn on it will remain the same. webcams or a video will have a new frame every time so we need to read the image again]
    #cv2.rectangle(img, (50, 192), (157, 240), (255,0,255), 2)
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255,0,255), 2) #draw rectangle on the image to mark the parking space
    
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick) #function to get the mouse click position
    cv2.waitKey(1)