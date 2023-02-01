#blue detection
import cv2
import numpy as np
import time
# Same command function as streaming, its just now we pass in the file path, nice!
cap = cv2.VideoCapture('results/output4.avi')
def friendlydetection(imageFrame):
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for color and
    # define mask
    blue_lower = np.array([90, 125, 70], np.uint8)
    blue_upper = np.array([128, 245, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)


    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                            mask = blue_mask)


    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(blue_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        
        if(area > 2000):
            
            x, y, w, h = cv2.boundingRect(contour)
            print('girdi mavi')
            return (x, y, w, h)
        else:
            return None

# FRAMES PER SECOND FOR VIDEO

# Always a good idea to check if the video was acutally there
# If you get an error at thsi step, triple check your file path!!
if cap.isOpened()== False: 
    print("Error opening the video file. Please double check your file path for typos. Or move the movie file to the same location as this script/notebook")

def friendlydetection(frame):
    imageFrame = frame.copy()
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for color and
    # define mask
    blue_lower = np.array([90, 125, 70], np.uint8)
    blue_upper = np.array([128, 245, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)


    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                            mask = blue_mask)


    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(blue_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 2000):
            x, y, w, h = cv2.boundingRect(contour)
            return (x, y, w, h)
        else:
            return None

# While the video is opened
while cap.isOpened():
    
    
    # Read the video file.
    ret, imageFrame = cap.read()
    
    # If we got frames, show them.
    if ret == True:

        bbox = friendlydetection(imageFrame)
        if bbox is not None:

            x, y, w, h = bbox
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                        (x + w, y + h),
                                        (255, 0, 0), 2)
            



    
        
        
        
         # Display the frame at same frame rate of recording
        # Watch lecture video for full explanation
      
        cv2.imshow('frame',imageFrame)
 
        # Press q to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            
            break
 
    # Or automatically break this whole loop if the video is over.
    else:
        break
        
cap.release()
# Closes all the frames
cv2.destroyAllWindows()