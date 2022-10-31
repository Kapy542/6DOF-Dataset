#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: Lots of tests to verify sync between mocap and rgb

from ImgReader import ImgReader
from utils import read_csv
import numpy as np
import cv2
import os

take_folder = "/home/kapyla/Desktop/KandiVol2/6DOF_Calibration_testing/CameraData"
take_name = "cal_1"
CHECKERBOARD = (7,5)

take_path = os.path.join(take_folder, take_name)

img_reader = ImgReader(take_path)

if len(img_reader.img_list_0) == 0:
    print("ERROR: no images in", take_path)
    #return
       
data = img_reader.idx_data
imgs0 = img_reader.img_list_0
imgs1 = img_reader.img_list_1

cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.resizeWindow('window', (1200, 1920))

img = cv2.imread("test.jpg")
#img = img_reader.img_1

# Detector
params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 1
params.maxThreshold = 255

# params.filterByConvexity = True
# params.minConvexity = 0.4

params.filterByArea = True
params.minArea = 10 #50
params.maxArea = 1000 #300

params.filterByInertia = True
params.minInertiaRatio = 0.1 #0.5

params.filterByCircularity = True
params.minCircularity = 0.4 #0.8

params.minDistBetweenBlobs = 1 #7

detector = cv2.SimpleBlobDetector_create(params)
    

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.findCirclesGrid(gray, (7,5)) 
ret, corners = cv2.findCirclesGrid(gray, CHECKERBOARD, None, flags=(cv2.CALIB_CB_SYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING),blobDetector=detector)
#cv2.imshow('window', gray)
#key = cv2.waitKey(0)

#while True:
##while img_reader.imgs_left:
#    img_reader.step()
#    img = img_reader.img
#    cv2.imshow('window', img)
##    cv2.waitKey(0)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break   
#
#cv2.destroyAllWindows()
#del img_reader



#%% Extract calibration images

# Initialize variables

# Get good frames from the mocap (middle of the stationary period) (mocap.py)

# Go through the images in a for loop

    # Check if img is good (checker_calibration.py)
    
    # Try calibration only with this one?
    
    # If previous succesfull: add to the list
    
# Parse some of the images? Coverage

# Save everything in the list (imgs, blob coordinates, mocap coordinates)
    
    
#%% Calibrate

# 