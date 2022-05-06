import cv2
import numpy as np
import codes.computer_vision.flag_detection as flag_detection
import codes.computer_vision.logo_detection as logo_detection
import codes.database as db
from codes.computer_vision.frame_class import frameClass

def main(aslan_frame_obj, anka_frame_obj, view_frame_obj):

    logo_detection.main(aslan_frame_obj, anka_frame_obj, view_frame_obj)

    if view_frame_obj.logo_label == 'friendly':
        flag_detection.detect_yellow_bbox(view_frame_obj)
    
    draw_bbox(view_frame_obj)

def draw_bbox(view_frame_obj):
    if view_frame_obj.logo_bbox is not None:
        color = (255, 100, 0) if view_frame_obj.logo_label == 'friendly' else (100, 0, 255)
        cv2.polylines(view_frame_obj.frame, [view_frame_obj.logo_bbox], True, color, 1, cv2.LINE_AA)

        if view_frame_obj.flag_bbox is not None:
            bbox_color = view_frame_obj.flag_bbox
            cv2.rectangle(view_img, (bbox_color[0], bbox_color[1]), (bbox_color[2], bbox_color[3]),(255, 0, 255), 2)
    

def create_logo_obj():
    logo_feature_detector = logo_detection.surf()

    aslan_frame = cv2.imread(db.aslan_path)
    db.aslan_frame_obj = frameClass(frame= aslan_frame, logo_label ='friendly', percentage=95)
    logo_detection.detect_features(logo_feature_detector, db.aslan_frame_obj)

    anka_frame = cv2.imread(db.anka_path)
    db.anka_frame_obj = frameClass(frame= anka_frame, logo_label ='enemy', percentage=95)
    logo_detection.detect_features(logo_feature_detector, db.anka_frame_obj)

    


    
    

    

