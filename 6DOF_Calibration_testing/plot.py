#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt
import numpy as np
import cv2
import matplotlib.pyplot as plt
from funcs.ImgReader import ImgReader
from funcs.mocap import read_csv, get_xyz, get_checker_coords, get_stationary_frames
from funcs.checker_calibration import create_detector, detect_points, draw_points, remove_outliers, order_checkerpoints, extract_2d
import os
import time
# %matplotlib qt


# Initialize paths
take_folder = "./"
take_name = "dotted_checker_1"

out_path = os.path.join(take_folder, "out")
take_path = os.path.join(take_folder, "CameraData", take_name)

take_name = os.path.split(take_path)[-1]
subject_name = take_name.split("_")[0]
out_dir = os.path.join(out_path, subject_name)


# Read MoCap data
df = read_csv(take_folder, take_name)

diffs, smooth_diffs, local_mins, diff_in_mins, local_maxs, diff_in_maxs = get_stationary_frames(df)

# Plot
x = np.arange(0, len(diffs))
plt.plot(x, diffs)
plt.plot(x, smooth_diffs, 'g')
plt.plot(local_mins, diff_in_mins, 'ro')
plt.plot(local_maxs, diff_in_maxs, 'bo')
plt.vlines(x = local_mins, ymin = 0, ymax = max(diffs),
           colors = 'red',
           label = 'Local mins')
plt.title("Checker movement")
plt.xlabel("Frame")
plt.ylabel("Absolute change in position")
plt.show()
