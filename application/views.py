# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MyFileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import os, sys
parser_classes = (MultiPartParser, FormParser)
import singlePhotoCrops
import getCropInfo
import time
from django.http import FileResponse
import operator
import json
import collections
import cv2

os.environ["MXNET_CUDNN_AUTOTUNE_DEFAULT"] = "0"

connString = 'dbname = tengri_db user = postgres password = postgres host = localhost port = 5432'
extension = '.jpg'
crop_size = 112
gpu_id = 0
flip = 0
det_threshold = 0.9
detection_model = 'models/detection/R50'
scales = [1080,1920]

img_size = '112,112'
recognition_model = 'models/recognition/model,0'
ga_model = ''
det = 0
threshold = 1.24

recognizer = getCropInfo.getPhotoInfo('crops/', 'crops/', 'media/', connString, extension, img_size, recognition_model, ga_model, gpu_id, det, flip, threshold)               
cropper = singlePhotoCrops.getCrops('media/', 'crops/', connString, extension, crop_size, gpu_id, flip, det_threshold, detection_model, scales, recognizer)

@api_view(['POST'])
def get_photo_align_large_files(request):
    if 'file' in request.data:      

        file_serializer = MyFileSerializer(data=request.data)
        if file_serializer.is_valid():
            [os.remove('media/' + f) for f in os.listdir('media/')]
            file_serializer.save()

        img_name = request.FILES[u'file'].name
        # Read original and save crops somewhere        
        try:
            [os.remove('crops/' + f) for f in os.listdir('crops/')]
            res = cropper.cropOriginal(45, 22, img_name)
            if res is not None:
                data = {'res': [i for i in range(len(res))]}            
            else:
                data = {'res' : None}
        except:
            data = {'test': 'failure'}
        # Read original and save crops somewhere
    return Response(data)


@api_view(['GET'])
def get_photo_align(request):    
    if request.method == 'GET':
        # Here we need change file paths
        choose = request.query_params.get('data')             
        file_path = 'crops/face_' + str(choose) + '.jpg'
        try:
            f = open(file_path, "rb")
            response = FileResponse(f)
        except:
            response_obj = {'error': 'File was not founded'}
            return Response(response_obj, status=204)
        return response

    response_obj = {'failed': 'no value of "data" with right order'}
    return Response(response_obj)


@api_view(['POST'])
def get_photo_metadata(request):
    if 'data' in request.POST:
        choose = request.POST.get('data')        
        # Read one crop and return json with top5 information
        file_path = 'face_' + str(choose) + '.jpg'
        data = recognizer.compareFeatures(file_path, '10.150.34.15', 3306, 'root', '')
        
        result_dict = dict()
        for r in data['person']:
            result_dict[r['fio']] = [r['feature'], r['udv_no'], r['iin'], r['fio']]

        od = collections.OrderedDict(sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True))

        return Response(od, status=200)                
        # Read one crop and return json with top5 information
    data = {'failed': 'no value of "data" with right order'}
    return Response(data)


@api_view(['GET'])
def get_photo_images(request):
    if request.method == 'GET':
        # Here we need to change file paths
        choose = request.query_params.get('data')             
        file_path = 'our_base/' + str(choose) + '.jpeg'
        try:
            f = open(file_path, "rb")
            response = FileResponse(f)
        except:
            response_obj = {'error': 'File was not founded'}
            return Response(response_obj, status=204)
        return response        

    response_obj = {'failed': 'no original image found for this person in database'}
    return Response(response_obj)


@api_view(['POST'])
def get_red_people(request):
    if 'file' in request.data:
        file_serializer = MyFileSerializer(data=request.data)

        if file_serializer.is_valid():
            [os.remove('media/' + f) for f in os.listdir('media/')]
            file_serializer.save()

        img_name = request.FILES[u'file'].name
        # Read original and save crops somewhere        
        try:
            [os.remove('crops/' + f) for f in os.listdir('crops/')]
            faces, landmarks = cropper.cropReds(img_name)  # singlePhotoCrops  
            data = {'res': [i for i in range(len(faces))]}
        except:
            data = {'res': 'failure, could not get crops'}
        # Read original and save crops somewhere
        if faces is not None:            
            data = recognizer.compareReds(img_name, 35, 14, faces, landmarks, '10.150.34.15', 3306, 'root', '')
            if data is not None:
                return Response(data, status=200)
            else:
                data = {'res': None}                
        else:            
            data = {'res': None}
        return Response(data, status=200)
        # Read one crop and return json with top5 information
    data = {'failed': 'No person found with right order'}
    return Response(data)


@api_view(['GET'])
def get_photo_red(request):
    if request.method == 'GET':
        # Here we need to change file paths
        choose = request.query_params.get('data')             
        file_path = 'our_base/' + str(choose) + '.jpeg'
        try:
            f = open(file_path, "rb")
            response = FileResponse(f)
        except:
            response_obj = {'error': 'File was not founded'}
            return Response(response_obj, status=204)
        return response        

    response_obj = {'failed': 'no original image found for this person in database'}
    return Response(response_obj)


@api_view(['GET'])
def get_photo_redbase(request):    
    if request.method == 'GET':
        # Here we need change file paths
        choose = request.query_params.get('data')           
        file_path = 'crops/face_' + str(choose) + '.jpg'
        try:
            f = open(file_path, "rb")
            response = FileResponse(f)
        except:
            response_obj = {'error': 'File was not founded'}
            return Response(response_obj, status=204)
        return response

    response_obj = {'failed': 'no value of "data" with right order'}
    return Response(response_obj)
