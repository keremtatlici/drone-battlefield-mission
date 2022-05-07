import numpy as np
import cv2
from matplotlib import pyplot as plt
import codes.database as db
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import traceback

def main(aslan_frame_obj, anka_frame_obj, view_frame_obj):

    view_feature_detector = surf(
    hessianThreshold=300,
    nOctaves=4, 
    nOctaveLayers=4,
    extended=True,
    keypointsRatio=0.01, 
    upright= False           
    )

    detect_features(view_feature_detector, view_frame_obj)
    view_kp_count = len(view_frame_obj.features['kp_cpu'])
    #print(view_kp_count)
    if view_kp_count < 300:
        return
    aslan_matches = matcher(aslan_frame_obj.features['des_gpu'], view_frame_obj.features['des_gpu']) 
    anka_matches = matcher(anka_frame_obj.features['des_gpu'], view_frame_obj.features['des_gpu'])

    aslan_good = good_matches(aslan_matches, factor=0.7)
    anka_good = good_matches(anka_matches, factor=0.7)

    #Logo Selection
    view_frame_obj.logo_label = logo_selection(aslan_good, anka_good, min_match_count=15)

    if view_frame_obj.logo_label == 'friendly':
        view_frame_obj.logo_bbox = detect_logo_bbox(aslan_frame_obj, view_frame_obj, aslan_good)
        view_frame_obj.logo_feature_count = len(aslan_good)
        
    elif view_frame_obj.logo_label == 'enemy':
        view_frame_obj.logo_bbox = detect_logo_bbox(anka_frame_obj, view_frame_obj, anka_good)
        view_frame_obj.logo_feature_count = len(anka_good)
    else: #CODE WILL END
        view_frame_obj.logo_bbox= None

def surf(
    hessianThreshold=300,
    nOctaves=4, 
    nOctaveLayers=2,
    extended=False,
    keypointsRatio=0.01, 
    upright= False
    ):

    feature_detector = cv2.cuda.SURF_CUDA_create(
        _hessianThreshold=hessianThreshold,
        _nOctaves=nOctaves,
        _nOctaveLayers=nOctaveLayers,
        _extended=extended,
        _keypointsRatio= keypointsRatio,
        _upright=upright,
        )

    return feature_detector




def detect_logo_bbox(logo_frame_obj, view_frame_obj, good):
    logo_features = logo_frame_obj.features
    view_features = view_frame_obj.features

    src_pts = np.float32([ logo_features['kp_cpu'][m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ view_features['kp_cpu'][m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

    matchesMask = mask.ravel().tolist()
    h,w = logo_frame_obj.frame.shape[:2]
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    return np.int32(dst)

def detect_features(feature_detector, frame_obj):
    features = dict()
    frame_obj.update_gpu_frame()

    img_gpu_gray = cv2.cuda.cvtColor(frame_obj.gpu_frame, cv2.COLOR_BGR2GRAY)

    features['kp_gpu'], features['des_gpu'] = feature_detector.detectWithDescriptors(img_gpu_gray, None)

    features['kp_cpu'] = cv2.cuda_SURF_CUDA.downloadKeypoints(feature_detector, features['kp_gpu'])
    
    frame_obj.features = features

def matcher(des_logo, des_view):
    matcher = cv2.cuda.DescriptorMatcher_createBFMatcher(cv2.NORM_L2)
    matches = matcher.knnMatch(des_logo, des_view, k=2)
    return matches

def good_matches(matches, factor=0.7):
    good = list()
    for m,n in matches:
        if m.distance < factor*n.distance:
            good.append(m)
    return good

def is_bbox_include_coordinate(bbox, coordinate):
    """
    bbox: list(list(x,y))[4]
    coordinate: list(x,y)
    return :Bool whether coordinate inside of the poligon
    """
    bbox = np.squeeze(bbox)
    point= Point(coordinate[0], coordinate[1])
    if bbox.shape == (4,2):
        polygon = Polygon([(bbox[0][0], bbox[0][1]), (bbox[1][0], bbox[1][1]), (bbox[2][0], bbox[2][1]), (bbox[3][0], bbox[3][1])])
        return polygon.contains(point)
    elif bbox.shape == (4,):

        xmin = bbox[0]
        ymin= bbox[1]
        width= xmin+bbox[2]
        height= ymin+bbox[3]
        polygon = Polygon([(xmin, ymin), (xmin+width, ymin), (xmin+width, ymin+height), (xmin, ymin+height)])
        return polygon.contains(point)
    else:
        return False

def logo_selection(aslan_good, anka_good, min_match_count=10):
    if len(aslan_good) > len(anka_good):
        if len(aslan_good) >= min_match_count:
            return 'friendly'
        else:
            return 'nolabel'
    else:
        if len(anka_good) >= min_match_count:
            return 'enemy'
        else:
            return 'nolabel'

def make_coordinates_bbox(coordinates):
    coordinates = np.squeeze(coordinates)
    x_list = [coordinates[0][0], coordinates[1][0],coordinates[2][0],coordinates[3][0]]
    y_list = [coordinates[0][1], coordinates[1][1],coordinates[2][1],coordinates[3][1]]
    xmin = min(x_list)
    xmax = max(x_list)

    ymin = min(y_list)
    ymax = max(y_list)
    bbox = np.array([xmin, ymin, xmax-xmin, ymax-ymin])
    return bbox