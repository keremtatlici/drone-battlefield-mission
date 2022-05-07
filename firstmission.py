
from codes.computer_vision.frame_class import frameClass
import cv2
import codes.database as db
import matplotlib.pyplot as plt
from codes.computer_vision import cv_main
import time
import codes.videoio as videoio
import traceback


def main():
    cv_main.create_logo_obj()


    """
    start_time = time.time()
    view_frame = cv2.imread(db.view_anka1_path)
    view_frame_obj = frameClass(view_frame)

    cv_main.main(db.aslan_frame_obj, db.anka_frame_obj, view_frame_obj)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(view_frame_obj.logo_feature_count)
    plt.imshow(view_frame_obj.frame)
    plt.show()

    """

    video_cap, height, width = videoio.get_video_cap(db.video1_path)
    #video_cap, height, width = videoio.get_cam_cap()

    count = -1

    while video_cap.isOpened() and db.first_mission:
        start_time = time.time()
        count +=1
        count_zero_filled = str(count).zfill(5)

        ret, frame = video_cap.read()

        if not ret:
            break

        view_frame_obj = frameClass(frame)

        try:
            cv_main.main(db.aslan_frame_obj, db.anka_frame_obj, view_frame_obj)
            #print(view_frame_obj.logo_bbox)
        except:
            print(f'{count}. FRAME => EXCEPTION IN MAIN.PY : OBJECT DETECTION MAIN ERROR')
            traceback.print_exc()


        if view_frame_obj.logo_label == 'friendly':
            color = (255, 100, 0)
        elif view_frame_obj.logo_label == 'enemy':
            color = (100, 0, 255)
        else:
            color = (100, 100, 100)

        if view_frame_obj.flag_label == 'yellowflag':
            is_yellow_flag = 'YES' 
        else:
            is_yellow_flag = 'NO'   
        
        fps = videoio.calculate_fps(start_time, num_frames=1)
        cv2.putText(frame, 'fps:'+fps, (5, 30), db.font, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'feature:'+str(view_frame_obj.logo_feature_count), (100, 30), db.font, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'label: '+view_frame_obj.logo_label, (5, 60), db.font, 0.8, color, 2, cv2.LINE_AA)
        cv2.putText(frame, 'is_center: '+str(view_frame_obj.is_logo_bbox_at_center), (5, 90), db.font, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'first aid needed?  '+str(is_yellow_flag), (5, 120), db.font, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('window', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    video_cap.release()
    cv2.destroyAllWindows()

    

        