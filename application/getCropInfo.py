import os
import cv2
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), 'facer'))
import face_model_tengri
from retinaface import RetinaFace
sys.path.append(os.path.join(os.path.dirname(__file__), 'db'))
import db_work
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), 'imager'))
import imager


class getPhotoInfo:
    def __init__(self, folder_to_read, folder_to_write, media_folder, connString, file_extension, image_size, model, ga_model, gpu_id, det_type, flip, threshold):
        self.folder_to_read = folder_to_read
        self.folder_to_write = folder_to_write
        self.media_folder = media_folder
        self.connString = connString
        self.file_extension = file_extension
        self.image_size = image_size
        self.model = model
        self.ga_model = ga_model
        self.gpu_id = gpu_id
        self.det_type = det_type
        self.flip = flip
        self.threshold = threshold
        self.superface = db_work.databaseWorker(self.connString, self.file_extension)
        self.modele = face_model_tengri.FaceModel(self.gpu_id, self.model, self.ga_model, self.threshold, self.det_type, self.flip, self.image_size)


    def resizeImg(self, img):     
        #width = int(img.shape[1] * scale_percent / 100)
        #height = int(img.shape[0] * scale_percent / 100)
        dim = (112, 112)
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        return resized


    def compareFeatures(self, image, hst, prt, usr, pwd):    
        img = cv2.imread(self.folder_to_read + '/' + image)               
        res = None
        feature = None
        
        face = self.modele.get_input(img)
        feature = self.modele.get_feature(face)                       
        '''
        try:
          face = self.modele.get_input(img)
          feature = self.modele.get_feature(face)                              
        except:
          print('Could not get feature. Bad face cropped!')
        '''
        data = None                
        res = self.superface.getSimilarity5(feature, hst, prt, usr, pwd)
        if res != None:
          data = {"person": []}
          for i in range(len(res)):                                             
            dct = {
                    "udv_no": res[i]['udv_no'],
                    "iin": res[i]['iin'],
                    "fio": res[i]['fio'],
                    "feature": res[i]['score']
                  }
            data['person'].append(dct)
          '''                    
          try:
            with open(self.folder_to_write + '/result.pickle', 'wb') as handle:
              pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL) # dct -> res
              print('Pickle ready')                    
          except:
            print('Could not write to a specified file')

          try:
            with open(self.folder_to_write + '/go_final.txt', 'wb') as f:
              f.write(image)
              print('Text file is ready')                    
          except:
            print('Could not write to a specified file')
          '''
        return data                      


    def compareReds(self, img, x_pixel, y_pixel, faces, landmarks, hst, prt, usr, pwd):        
        shower = imager.imViewer(112, 2)
        data = {"person": []}
        if faces is not None:
            print('Found [' + str(faces.shape[0]) + '] face(s)')            
            for i in range(faces.shape[0]):
                image = cv2.imread(os.path.join(self.media_folder, img))                     
                box = faces[i].astype(np.int)                       
                # Set filename
                # filename = image.split(',')[0] # str(datetime.datetime.now()).replace(":", "_").replace(".", "_").replace("-", "_").replace(' ', '_')
                # dt = datetime.date.today()
                # tm = datetime.datetime.now().strftime("%H:%M:%S")
                # Getting the size of head rectangle
                height_y = box[3] - box[1]
                width_x = box[2] - box[0]
                # Calculating cropping area                
                res = None                
                if height_y > x_pixel and width_x > y_pixel and (height_y/float(width_x)) < 1.8:
                    center_y = box[1] + ((box[3] - box[1])/2)   # calculating center of the x side
                    center_x = box[0] + ((box[2] - box[0])/2)   # calculating center of the y side
                    rect_y = center_y - height_y/2              # calculating starting x of rectangle
                    rect_x = center_x - width_x/2               # calculating starting y of rectangle                    
                    # Cropping an area
                    cropped_img = image[rect_y:rect_y+height_y,rect_x:rect_x+width_x] 
                    # strange                                                                              
                    resize = self.resizeImg(cropped_img)                    
                    face = self.modele.get_input(resize)
                    feature = self.modele.get_feature(face)
                    res = self.superface.getSimilarityTest(feature, hst, prt, usr, pwd)
                    if len(res) > 0:
                      # print(len(res))
                      res_img = shower.drawRect(image, rect_x, rect_y, width_x, height_y, 5)
                      cv2.imwrite(self.folder_to_write + '/face_' + str(i) + '.jpg', res_img)                                                                   
                      dct = {
                              "id": i,
                              "fio": res[0]['fio'],
                              "red_id": res[0]['red_id'],
                              "info": res[0]['info'],
                              "score": res[0]['score']
                            }                      
                      data["person"].append(dct)                                                    
                    # print('strange')
                    # print('face ' + str(i) + ' was written')
                    done = True                  
                else:                                      
                    print('Face is too small or modified or in sharp angle')
                    done = True
        else:
            print('No faces')
            done = True
        return data                       
            # [os.remove(self.folder_to_read + '/' + f) for f in os.listdir(self.folder_to_read)] 