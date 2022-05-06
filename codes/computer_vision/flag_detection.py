import numpy as np
import cv2


def detect_yellow_bbox(view_img_obj):
    imageFrame = view_img_obj.frame.copy()
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([22, 120, 0], np.uint8)
    red_upper = np.array([45, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    kernal = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame,
                            mask = red_mask)

    contours, hierarchy = cv2.findContours(red_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            #imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h),(255, 0, 0), 2)    
            bbox = (x, y, x+w, y+h)
            view_img_obj.flag_bbox =bbox
            view_img_obj.flag_label='yellowflag'
