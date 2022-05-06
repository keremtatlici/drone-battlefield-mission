import numpy as np
import cv2


class frameClass():
    def __init__(self, frame, logo_label="nolabel", percentage=0):
        """
        frame : np.array
        height : int
        width : int
        center_coordinate : np.array[2]
        """
        self.update_frame(frame)
        self.logo_label =logo_label # enemy, friendly, nolabel
        self.logo_bbox = None        
        self.flag_label = "nolabel" # yellowflag, nolabel
        self.flag_bbox = None
        self.features = None
        self.is_logo_bbox_at_center=False
        self.is_flag_bbox_at_center=False
        self.logo_feature_count=0
        if percentage is not 0:
            self.manipulate_image_size(percentage)

    def update_center_coordinate(self):
        self.center_coordinate = np.array([int(self.width/2), int(self.height/2)])
    
    def update_frame(self, frame):
        """
        frame : np.array
        """
        self.frame = frame
        self.update_dimention()
        self.update_center_coordinate()

    def update_gpu_frame(self):
        self.gpu_frame = cv2.cuda_GpuMat(self.frame)

    def update_dimention(self):
        self.height = self.frame.shape[0]
        self.width = self.frame.shape[1]

    def manipulate_image_size(self, percentage):
        """
        percentage : int
        """
        scale_percent = 100 - percentage
        width = int(self.width * scale_percent / 100)
        height = int(self.height * scale_percent / 100)
        dim = (width, height)
        size_changed_img = cv2.resize(self.frame, dim, interpolation = cv2.INTER_AREA)
        self.update_frame(size_changed_img)
