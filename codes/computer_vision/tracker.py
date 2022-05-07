import cv2
import copy
import codes.database as db
import codes.computer_vision.logo_detection as logo_detection
import numpy as np

def main(view_frame_obj):
    if db.tracker is None:
        tracker_init(db.prev_frame_obj)

    ok, logo_bbox = db.tracker.update(db.prev_frame_obj.frame)
    if ok:
        xmin = int(logo_bbox[0])
        ymin = int(logo_bbox[1])
        width = int(logo_bbox[0] + logo_bbox[2])
        height = int(logo_bbox[1] + logo_bbox[3])
        logo_bbox = np.array([xmin, ymin, width, height])
        view_frame_obj.logo_bbox = logo_bbox
        db.prev_frame_obj = copy.copy(view_frame_obj)
        view_frame_obj.is_logo_bbox_at_center = logo_detection.is_bbox_include_coordinate(logo_bbox, view_frame_obj.center_coordinate)
        print(view_frame_obj.is_logo_bbox_at_center)
        if not view_frame_obj.is_logo_bbox_at_center:
            db.prev_frame_obj.logo_label='nolabel'
            db.tracker= None
    else:
        db.tracker = None
        view_frame_obj.logo_bbox = None
        view_frame_obj.logo_label = "nolabel"
        db.prev_frame_obj = copy.copy(view_frame_obj)

def tracker_init(prev_frame_obj):
    tracker = cv2.legacy.TrackerMOSSE_create()
    logo_bbox = prev_frame_obj.logo_bbox
    logo_bbox = logo_detection.make_coordinates_bbox(logo_bbox) if len(logo_bbox.shape) == 3 else logo_bbox
    logo_bbox = tuple([logo_bbox[0], logo_bbox[1], logo_bbox[2], logo_bbox[3]])
    tracker.init(prev_frame_obj.frame, logo_bbox)
    db.tracker = tracker
