import os
import cv2
import sys
import numpy as np
import datetime
import imutils
sys.path.append(os.path.join(os.path.dirname(__file__), 'facer'))
import face_model_tengri
from retinaface import RetinaFace
sys.path.append(os.path.join(os.path.dirname(__file__), 'db'))
import db_work
import shutil



class getCrops:
    def __init__(self, folder_to_read, folder_to_write, connString, file_extension, image_size, gpu_id, flip, det_threshold, detection_model, scales, rec_model):
        self.folder_to_read = folder_to_read
        self.folder_to_write = folder_to_write
        self.connString = connString
        self.file_extension = file_extension
        self.image_size = image_size
        self.gpu_id = gpu_id
        self.flip = flip
        self.det_threshold = det_threshold
        self.det_model = detection_model
        self.scales = scales
        self.detector = RetinaFace(self.det_model, 0, self.gpu_id, 'net3')
        self.rec_model = rec_model


    def resizeImg(self, img):     
        #width = int(img.shape[1] * scale_percent / 100)
        #height = int(img.shape[0] * scale_percent / 100)
        dim = (self.image_size, self.image_size)
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        return resized

    def cleanFolder(self, folder):        
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


    def cropOriginal(self, x_pixel, y_pixel, image):
        count = 1
        # [os.remove(self.folder_to_write + '/' + f) for f in os.listdir(self.folder_to_write)]                  
        done = False
        img = cv2.imread(self.folder_to_read + '/' + image)
        thresh = self.det_threshold
        im_shape = img.shape
        # print(im_shape)
        scales = self.scales
        ################ NEW #################
        scales = list(im_shape[0:2])
        target_size = scales[0]
        max_size = scales[1]
        im_size_min = np.min(im_shape[0:2])
        im_size_max = np.max(im_shape[0:2])        
        im_scale = float(target_size) / float(im_size_min)
        # prevent bigger axis from being more than max_size:
        if np.round(im_scale * im_size_max) > max_size:
            im_scale = float(max_size) / float(im_size_max)                 
        
        scales = [im_scale]        
        flip = False
        for c in range(count):
            faces, landmarks = self.detector.detect(img, thresh, scales=scales, do_flip=flip)

        result = []
        if faces is not None:
            print('Found [' + str(faces.shape[0]) + '] face(s)')
            for i in range(faces.shape[0]):                     
                box = faces[i].astype(np.int)                       
                # Set filename
                filename = image.split(',')[0] # str(datetime.datetime.now()).replace(":", "_").replace(".", "_").replace("-", "_").replace(' ', '_')
                dt = datetime.date.today()
                tm = datetime.datetime.now().strftime("%H:%M:%S")
                # Getting the size of head rectangle
                height_y = box[3] - box[1]
                width_x = box[2] - box[0] 
                # print('Height: ' + str(height_y) + ' Width: ' + str(width_x))
                # Calculating cropping area
                # print(landmarks)
                if height_y > x_pixel and width_x > y_pixel and (height_y/float(width_x)) < 1.8:
                    center_y = box[1] + ((box[3] - box[1])/2)   # calculating center of the x side
                    center_x = box[0] + ((box[2] - box[0])/2)   # calculating center of the y side
                    rect_y = center_y - height_y/2              # calculating starting x of rectangle
                    rect_x = center_x - width_x/2               # calculating starting y of rectangle
                    # Cropping an area
                    cropped_img = img[rect_y:rect_y+height_y,rect_x:rect_x+width_x]
                    resize = self.resizeImg(cropped_img)                    
                    cv2.imwrite(self.folder_to_write + '/face_' + str(i) + '.jpg', resize)
                    result.append(i)
                    print('face ' + str(i) + ' was written')
                    done = True                  
                else:
                    print('Face is too small or modified or in sharp angle')
                    done = True
        else:
            result = None
            print('No faces')
            done = True                       
        '''
        if done:
            with open('results/go_res.txt', 'wb') as f:
                f.write(filename)
            # [os.remove(self.folder_to_read + '/' + f) for f in os.listdir(self.folder_to_read)]        
        '''
        return result
                                                                        

    def cropReds(self, image):
        count = 1
        # [os.remove(self.folder_to_write + '/' + f) for f in os.listdir(self.folder_to_write)]                  
        done = False
        img = cv2.imread(self.folder_to_read + '/' + image)
        thresh = self.det_threshold
        im_shape = img.shape
        # print(im_shape)
        scales = self.scales
        ################ NEW #################
        scales = list(im_shape[0:2])
        target_size = scales[0]
        max_size = scales[1]
        im_size_min = np.min(im_shape[0:2])
        im_size_max = np.max(im_shape[0:2])        
        im_scale = float(target_size) / float(im_size_min)
        # prevent bigger axis from being more than max_size:
        if np.round(im_scale * im_size_max) > max_size:
            im_scale = float(max_size) / float(im_size_max)                 
        
        scales = [im_scale]        
        flip = False
        for c in range(count):
            faces, landmarks = self.detector.detect(img, thresh, scales=scales, do_flip=flip)        
        return faces, landmarks