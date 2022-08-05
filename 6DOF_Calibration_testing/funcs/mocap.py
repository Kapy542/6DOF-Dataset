#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas  

def read_csv(take_folder, take_name):
    path = os.path.join(take_folder, "opti", take_name) + ".csv"
    df = pandas.read_csv(path, header=[2,5])
    return df

# Exctract marker's 3d position from dataframe
def get_xyz(idx, idx_x, idx_y, df):
    col = "checker:" + str(idx_x) + "_" + str(idx_y)
    cols = df.xs(col, axis=1)
    xs = cols.xs('X', axis=1)
    ys = cols.xs('Y', axis=1)
    zs = cols.xs('Z', axis=1)
    xyz = np.array( [xs[idx], ys[idx], zs[idx]] )
    return xyz

# Get all checker marker coordinates on particular index
def get_checker_coords(idx, df):
    coords = np.zeros([5*7,3])
    for x in range(0,7):
        for y in range(0,5):
            xyz = get_xyz(idx, x+1, y+1, df)
            coords[5*y+x,:] = xyz
    return coords

# Check whether all points exists in MoCap data for this frame
def checker_points_exists():
    return False

# Is this frame good for calibration based on MoCap data
def is_good_frame():
    return False