
from codes.computer_vision.frame_class import frameClass
import cv2
import codes.database as db
import matplotlib.pyplot as plt
from codes.computer_vision import cv_main
import time
import codes.videoio as videoio
import traceback
import numpy as np
import codes.communication.arduino_comm as arduino_comm
from threading import Thread



def zoom_cam(frame,percent=50):
    #get the webcam size
    height, width, channels = frame.shape

    #prepare the crop
    centerX,centerY=int(height/2),int(width/2)
    radiusX,radiusY= int(percent*height/200),int(percent*width/200)

    minX,maxX=centerX-radiusX,centerX+radiusX
    minY,maxY=centerY-radiusY,centerY+radiusY

    cropped = frame[minX:maxX, minY:maxY]
    resized_cropped = cv2.resize(cropped, (width, height))
    return resized_cropped

def yellowdetection(imageFrame):
    bbox_list=[]
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set ranQQge for color and
    # define mask
    yellow_lower = db.yellow_lower
    yellow_upper = db.yellow_upper
    blue_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)


    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((1, 1), "uint8")

    # For red color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                            mask = blue_mask)


    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(blue_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    my_contour=None
    bbox=None
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 2000 and area> max_area:
            my_contour = contour
            max_area = area
            
    if my_contour is not None:
        bbox = cv2.boundingRect(my_contour)
        
    return bbox
def enemydetection(imageFrame):
    bbox_list=[]
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set ranQQge for color and
    # define mask
    red_lower = db.red_lower
    red_upper = db.red_upper
    blue_mask = cv2.inRange(hsvFrame, red_lower, red_upper)


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
    max_area = 0
    my_contour=None
    bbox=None
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 1000 and area> max_area:
            my_contour = contour
            max_area = area
            
    if my_contour is not None:
        bbox = cv2.boundingRect(my_contour)
        
    return bbox


def friendlydetection(imageFrame):
    bbox_list=[]
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set ranQQge for color and
    # define mask
    blue_lower = db.blue_lower
    blue_upper = db.blue_upper
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
    max_area = 0
    my_contour=None
    bbox=None
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 2000 and area> max_area:
            my_contour = contour
            max_area = area
            
    if my_contour is not None:
        bbox = cv2.boundingRect(my_contour)
        
    return bbox


def objectdetection(frameObj):
    frame = frameObj.frame

    yellow_bbox = yellowdetection(frame)
    friendly_bbox = friendlydetection(frame)
    enemy_bbox = enemydetection(frame)

    if enemy_bbox is not None:
        #print('enemy!!!')
        frameObj.logo_label='enemy'
        frame = cv2.rectangle(
            frame,
            (enemy_bbox[0], enemy_bbox[1]),
            (enemy_bbox[0]+enemy_bbox[2], enemy_bbox[1]+ enemy_bbox[3]),
            (0, 0, 255), 2)

    if friendly_bbox is not None:
        #print('friendly!!!')
        frameObj.logo_label='friendly'
        frame = cv2.rectangle(
            frame,
            (friendly_bbox[0], friendly_bbox[1]),
            (friendly_bbox[0]+friendly_bbox[2], friendly_bbox[1]+ friendly_bbox[3]),
            (255, 0, 0), 2)

        if yellow_bbox is not None:
            #print('yellowflag!!!')
            frameObj.flag_label='yellowflag'
            frame = cv2.rectangle(
                frame,
                (yellow_bbox[0], yellow_bbox[1]),
                (yellow_bbox[0]+yellow_bbox[2], yellow_bbox[1]+ yellow_bbox[3]),
                (0, 255, 0), 2)

    frameObj.update_frame(frame)

        


def main():
    #cv_main.create_logo_obj()
    airstrike_process = Thread(target=arduino_comm.send_message, args=(db.arduino, "0"))
    sos_process = Thread(target=arduino_comm.send_message, args=(db.arduino, "1"))
    #video_cap, height, width = videoio.get_video_cap("results/output4.avi")
    video_cap, height, width = videoio.get_cam_cap()

    what_time_is_it = videoio.what_time_is_it()
    video_writer = videoio.get_video_writer(video_cap, 30 , db.save_root_path+ what_time_is_it +'.avi', frame_width=640, frame_height=360)
    count = -1

    while video_cap.isOpened() and db.first_mission:
        start_time = time.time()
        #time.sleep(0.010)
        count +=1
        count_zero_filled = str(count).zfill(5)

        ret, frame = video_cap.read()

        if not ret:
            break
            
        view_frame_obj = frameClass(frame, percentage=50)

        try:
            objectdetection(view_frame_obj)
        except:
            print(f'{count}. FRAME => EXCEPTION IN MAIN.PY : OBJECT DETECTION MAIN ERROR')
            traceback.print_exc()
        #cv2.imwrite(db.save_root_path+'constrat_method1.png', frame)
        
        #print(view_frame_obj.frame.shape)
        

        


        if view_frame_obj.logo_label == 'friendly':
            color = (255, 100, 0)
        elif view_frame_obj.logo_label == 'enemy':
            if not airstrike_process.is_alive():
                airstrike_process = Thread(target=arduino_comm.send_message, args=(db.arduino, "0"))
                airstrike_process.start()
            color = (100, 0, 255)
        else:
            color = (100, 100, 100)

        if view_frame_obj.flag_label == 'yellowflag':
            is_yellow_flag = 'YES' 
            if not sos_process.is_alive():
                sos_process = Thread(target=arduino_comm.send_message, args=(db.arduino, "1"))
                sos_process.start()

        else:
            is_yellow_flag = 'NO'   
        
        fps = videoio.calculate_fps(start_time, num_frames=1)
        cv2.putText(view_frame_obj.frame, 'fps:'+fps, (5, 30), db.font, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        
        cv2.putText(view_frame_obj.frame, 'feature:'+str(view_frame_obj.logo_feature_count), (100, 30), db.font, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(view_frame_obj.frame, 'label: '+view_frame_obj.logo_label, (5, 60), db.font, 0.8, color, 2, cv2.LINE_AA)
        cv2.putText(view_frame_obj.frame, 'is_center: '+str(view_frame_obj.is_logo_bbox_at_center), (5, 90), db.font, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(view_frame_obj.frame, 'first aid needed?  '+str(is_yellow_flag), (5, 120), db.font, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        
        db.liveframe = view_frame_obj
        video_writer.write(view_frame_obj.frame)
        cv2.imshow('window', view_frame_obj.frame)

        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    video_cap.release()
    
    cv2.destroyAllWindows()
    video_writer.release()
    


















    ##########OLD

    """
def friendlydetection(imageFrame):
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set ranQQge for color and
    # define mask
    blue_lower = db.blue_lower
    blue_upper = db.blue_upper
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)


    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((17, 17), "uint8")

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
"""

"""
def enemydetection(imageFrame):
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and
    # define mask
    red_lower = db.red_lower
    red_upper = db.red_upper
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)


    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_der = cv2.bitwise_and(imageFrame, imageFrame,
                            mask = red_mask)


    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        
        if(area > 300):
            
            x, y, w, h = cv2.boundingRect(contour)
            return (x,y,w,h)
        else:
            return None
"""


"""
def yellowdetection(imageFrame):
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and
    # define mask
    yellow_lower = db.yellow_lower
    yellow_upper = db.yellow_upper
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)


    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((1, 1), "uint8")

    # For red color
    yellow_mask = cv2.dilate(yellow_mask, kernal)
    res_yellow = cv2.bitwise_and(imageFrame, imageFrame,
                            mask = yellow_mask)


    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(yellow_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        
        if(area > 1):
            x, y, w, h = cv2.boundingRect(contour)
            return (x,y,w,h)
        else:
            return None

"""