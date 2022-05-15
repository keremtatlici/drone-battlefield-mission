import cv2
from codes.computer_vision.frame_class import frameClass

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

first_mission = True
second_mission=False

error_message="hatalı mesaj"
ip = "192.168.137.104"

liveframe = prev_frame_obj
normalframe = None
telemetri = None

vehicle = None

