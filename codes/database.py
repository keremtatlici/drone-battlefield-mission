import cv2
from codes.computer_vision.frame_class import frameClass
import numpy as np

logos_root_path='datasets/logos/'
views_root_path='datasets/views/'
save_root_path = 'results/'

aslan_path = logos_root_path+'aslan.png'
anka_path = logos_root_path+'anka.png'
temp_img = cv2.imread(aslan_path)

view_aslan1_path = views_root_path+'aslan1.png'
view_anka1_path = views_root_path+'anka1.png'

video1_path = views_root_path+'simulation.MOV'
video2_path = views_root_path+'simulation2.MOV'
video3_path = views_root_path+'simulation3.MOV'

font = cv2.FONT_HERSHEY_SIMPLEX

aslan_frame_obj = None
anka_frame_obj =None

tracker = None

prev_frame_obj = frameClass(temp_img)

first_mission = False
second_mission=False

error_message="hatalı mesaj"
ip = "192.168.1.10"

liveframe = prev_frame_obj
normalframe = None
telemetri = None

vehicle = None
arduino = None

red_lower = np.array([160,100,20], np.uint8)
red_upper = np.array([179,255,255], np.uint8)
blue_lower = np.array([90, 125, 70], np.uint8)
blue_upper = np.array([128, 245, 255], np.uint8)
yellow_lower = np.array([22, 80, 0], np.uint8)
yellow_upper = np.array([45, 170, 255], np.uint8)

