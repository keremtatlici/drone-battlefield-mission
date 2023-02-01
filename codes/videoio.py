import cv2
import time
from datetime import datetime
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=2,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink sync=False"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
"""

"""
        "nvarguscamerasrc sensor-id=0 !"
        "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, framerate=(fraction)30/1 ! "
        "nvvidconv flip-method=2 ! "
        "video/x-raw, width=(int)960, height=(int)540, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink sync=False"
"""

"""
def gstreamer_pipeline():
    return (
                "nvarguscamerasrc sensor-id=0 !"
        "video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, framerate=(fraction)30/1 ! "
        "nvvidconv flip-method=2 ! "
        "video/x-raw, width=(int)640, height=(int)360, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink sync=False"
    )
"""

def gstreamer_pipeline():
    return (
        "nvarguscamerasrc sensor-id=0 !"
        "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=NV12, framerate=60/1 ! "
        "nvvidconv flip-method=2 ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink sync=False"
    )
#nvarguscamerasrc sensor_id=ID ! video/x-raw(memory:NVMM), width=X, height=Y, format=(string)NV12 ! nvvidconv flip-method=M ! video/x-raw, format=I420, appsink max-buffers=1 drop=true
#nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, framerate=(fraction)15/1 ! nvvidconv flip-method=2 ! videobalance contrast=1.5 brightness=-0.3 ! videoconvert ! video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=true
""" 
def gstreamer_pipeline():
    return "nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, framerate=(fraction)15/1 ! nvvidconv flip-method=2 ! videoconvert ! video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=true"
"""
def get_cam_cap():
    video_cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    height = video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    width =  video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return video_cap, height, width

def get_video_cap(video_path):
    video_cap = cv2.VideoCapture(video_path)
    height = video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    width =  video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return video_cap, height, width

def get_video_writer(video_cap, fps, path, frame_width= None, frame_height = None):
    if frame_height is None or frame_width is None:
        frame_width = int(video_cap.get(3))
        frame_height = int(video_cap.get(4))
    
    frame_size = (frame_width,frame_height)
    video_writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('M','J','P','G'), fps, frame_size)
    return video_writer  

def random_string(size=10):
    letters= string.ascii_letters
    return ( ''.join(random.choice(letters) for i in range(size)))

def calculate_fps(start_time, num_frames=1):
    end_time = time.time()
    seconds= end_time - start_time
    fps = num_frames / seconds
    return str(int(fps))

def what_time_is_it():
    what_time_is_it = datetime.now()
    what_time_is_it = str(what_time_is_it.year) +\
                '-' + str(what_time_is_it.month) +\
                '-' + str(what_time_is_it.day) +\
                '-' + str(what_time_is_it.hour) +\
                ':' + str(what_time_is_it.minute) +\
                ':' + str(what_time_is_it.second)
    return what_time_is_it