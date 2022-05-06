
from codes.computer_vision.frame_class import frameClass
import cv2
import codes.database as db
import matplotlib.pyplot as plt
from codes.computer_vision import cv_main
import time

cv_main.create_logo_obj()

start_time = time.time()
view_frame = cv2.imread(db.view_anka1_path)
view_frame_obj = frameClass(view_frame)

cv_main.main(db.aslan_frame_obj, db.anka_frame_obj, view_frame_obj)
print("--- %s seconds ---" % (time.time() - start_time))
print(view_frame_obj.logo_feature_count)
plt.imshow(view_frame_obj.frame)
plt.show()
