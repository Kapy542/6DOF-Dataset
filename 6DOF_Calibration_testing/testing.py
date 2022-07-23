#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt
import numpy as np
import cv2
import matplotlib.pyplot as plt
from funcs.ImgReader import ImgReader
from funcs.mocap import read_csv, get_xyz, get_checker_coords
from funcs.checker_calibration import create_detector, detect_points, draw_points
import argparse
import os

#%% Read img

take_name = "dotted_checker_1"
take_folder = "/home/kapyla/Desktop/KandiVol2/6DOF_Calibration_testing"
out_path = "/home/kapyla/Desktop/KandiVol2/6DOF_Calibration_testing/out"

take_path = os.path.join(take_folder, "CameraData", take_name)

df = read_csv(take_folder, take_name)

take_name = os.path.split(take_path)[-1]
subject_name = take_name.split("_")[0]
out_dir = os.path.join(out_path, subject_name)

idx = 600

img_reader = ImgReader(take_path)
img_reader.set_idx(idx)
img = img_reader.img_1
    
## Window setup
#cv2.namedWindow('window', cv2.WINDOW_NORMAL)
##cv2.resizeWindow('window', output_size)
#cv2.imshow("window", img)       
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = gray[400:900,80:700]
#cv2.namedWindow('window', cv2.WINDOW_NORMAL)
#cv2.imshow("window", gray)       
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#plt.imshow(img)

cal_data = []

thisdict =	{
  "idx": idx,
  "xy": (1,2),
  "xyz": get_checker_coords(idx, df),
  "img": img
}

cal_data.append(thisdict)
#del img_reader



detector = create_detector()
keypoints = detect_points(img, detector)
img_with_points = draw_points(img, keypoints)


cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.imshow("window", img_with_points)       
cv2.waitKey(0)
cv2.destroyAllWindows()
#plt.imshow(img_with_points)

#%% Detect dots

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = gray[400:900,80:700]
cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.imshow("window", gray)       
cv2.waitKey(0)
cv2.destroyAllWindows()

CHECKERBOARD = (7,5)


#%% Works somehow

# Standard imports
#import cv2
#import numpy as np;
#
## Read image
#im = cv2.imread("dots2.jpg")
im = gray

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 100
params.maxThreshold = 255

params.filterByColor = True
params.blobColor = 255 # Important

# Filter by Area.
params.filterByArea = True
params.minArea = 10
params.maxArea = 100

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.8

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.9

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.1

# Create a detector with the parameters
# OLD: detector = cv2.SimpleBlobDetector(params)
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()

