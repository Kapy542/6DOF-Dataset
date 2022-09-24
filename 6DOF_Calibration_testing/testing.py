#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt
import numpy as np
import cv2
import matplotlib.pyplot as plt
from funcs.ImgReader import ImgReader
from funcs.mocap import read_csv, get_xyz, get_checker_coords, get_good_frames
from funcs.checker_calibration import create_detector, detect_points, draw_points, remove_outliers, order_checkerpoints
import argparse
import os
# %matplotlib qt

#%% Read img

# Initialize paths
take_folder = "./"
take_name = "dotted_checker_1"
# take_folder = "/home/kapyla./Desktop/KandiVol2/6DOF_Calibration_testing"

out_path = os.path.join(take_folder, "out")
take_path = os.path.join(take_folder, "CameraData", take_name)

take_name = os.path.split(take_path)[-1]
subject_name = take_name.split("_")[0]
out_dir = os.path.join(out_path, subject_name)

# Read MoCap data
df = read_csv(take_folder, take_name)
good_frames = get_good_frames(df)
x = np.arange(0, len(good_frames))
plt.plot(x, good_frames)
#%%

idx = 180 # Hyvä kuva ilman motionblurria
#idx = 320 # Hyvä kuva ilman motionblurria
#idx = 446 # Hyvä kuva ilman motionblurria
#idx = 485 # Hyvä kuva ilman motionblurria
#idx = 500 # Hyvä kuva ilman motionblurria
#idx = 600 # Hyvä kuva ilman motionblurria
#idx = 824 # Hyvä kuva ilman motionblurria
#idx = 845 # Hyvä kuva ilman motionblurria
#idx = 862 # Hyvä kuva ilman motionblurria
#idx = 870 # Hyvä kuva ilman motionblurria
#idx = 200 # Motion blurria
#idx = 340 # Motion blurria
#idx = 360 # Motion blurria
idxs = [180,320,446,485,500,600,824,845,862,870]

# Img reader to read raw images
img_reader = ImgReader(take_path)
img_reader.set_idx(idx)
img = img_reader.img_1

# Create blob detector
detector = create_detector()
keypoints = detect_points(img, detector)
img_with_points = draw_points(img, keypoints)

cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.imshow("window", img_with_points)       
cv2.waitKey(0)
cv2.destroyAllWindows()
#plt.imshow(img_with_points)


parsed_keypoints = remove_outliers(keypoints)
ordered_keypoints = order_checkerpoints(parsed_keypoints)
img_with_points = draw_points(img, ordered_keypoints)

cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.imshow("window", img_with_points)       
cv2.waitKey(0)
cv2.destroyAllWindows()

del img_reader

#%% Detect dots

# CHECKERBOARD = (7,5)


# thisdict =	{
#   "idx": idx,
#   "xy": (1,2),
#   "xyz": get_checker_coords(idx, df),
#   "img": img
# }

# cal_data = []
# cal_data.append(thisdict)