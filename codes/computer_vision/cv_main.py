import cv2
import numpy as np
import codes.computer_vision.flag_detection as flag_detection
import codes.computer_vision.logo_detection as logo_detection
import codes.database as db
from codes.computer_vision.frame_class import frameClass
import codes.computer_vision.tracker as tracker
import copy

def main(aslan_frame_obj, anka_frame_obj, view_frame_obj):
    #print(db.prev_frame_obj.logo_label)
    #print(db.prev_frame_obj.is_logo_bbox_at_center)
    #print("##############################")
    if db.prev_frame_obj.logo_label is not "nolabel" and db.prev_frame_obj.is_logo_bbox_at_center:
        view_frame_obj.logo_label = db.prev_frame_obj.logo_label
        tracker.main(view_frame_obj)
    else: 
        logo_detection.main(aslan_frame_obj, anka_frame_obj, view_frame_obj)

    if view_frame_obj.logo_label == 'friendly':
        flag_detection.detect_yellow_bbox(view_frame_obj)
    

    draw_bbox(view_frame_obj)

def draw_bbox(view_frame_obj):
    logo_bbox = view_frame_obj.logo_bbox
    if logo_bbox is not None:
        view_frame_obj.is_logo_bbox_at_center = logo_detection.is_bbox_include_coordinate(logo_bbox, view_frame_obj.center_coordinate)
        db.prev_frame_obj = copy.copy(view_frame_obj)
        color = (255, 100, 0) if view_frame_obj.logo_label == 'friendly' else (100, 0, 255)
        if len(logo_bbox.shape) == 3:
            cv2.polylines(view_frame_obj.frame, [logo_bbox], True, color, 1, cv2.LINE_AA)
            #print(view_frame_obj.logo_feature_count)
        else:
            cv2.rectangle(view_frame_obj.frame, (logo_bbox[0], logo_bbox[1]), (logo_bbox[2], logo_bbox[3]),(255, 0, 255), 2)

        if view_frame_obj.flag_bbox is not None:
            bbox_color = view_frame_obj.flag_bbox
            cv2.rectangle(view_frame_obj.frame, (bbox_color[0], bbox_color[1]), (bbox_color[2], bbox_color[3]),(255, 0, 255), 2)
    

def create_logo_obj():
    logo_feature_detector = logo_detection.surf(
        hessianThreshold=300,
        nOctaves=4,
        nOctaveLayers=4,
        extended=True,
        keypointsRatio= 0.01,
        upright=False
    )

    aslan_frame = cv2.imread(db.aslan_path)
    db.aslan_frame_obj = frameClass(frame= aslan_frame, logo_label ='friendly', percentage=95)
    logo_detection.detect_features(logo_feature_detector, db.aslan_frame_obj)

    anka_frame = cv2.imread(db.anka_path)
    db.anka_frame_obj = frameClass(frame= anka_frame, logo_label ='enemy', percentage=95)
    logo_detection.detect_features(logo_feature_detector, db.anka_frame_obj)

    


    
    

    

