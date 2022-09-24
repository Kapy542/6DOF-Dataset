#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas  
import scipy.signal

FPS_MULT = 5

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

# TODO: Check sync between cams and optitrack (FPS_MULT)
# Change of position between frames and pick local_mins ?
# Get good frame idxs. Good frame = checker is not moving
# Get one index on the middle of stationary period
def get_good_frames(df):
    diffs = np.array([0])
    good_frames = np.array([0])
    bad_frames = np.array([0])
    prev_coords = get_checker_coords(0, df)
   
#    for idx in range(FPS_MULT, len(df), FPS_MULT):
    for idx in range(FPS_MULT, 2000, FPS_MULT):
        # Calculate absulute differnece in position from previous frame
        coords = get_checker_coords(idx, df)
        diff = np.abs( np.sum(prev_coords-coords) )
        diffs = np.append(diffs, diff)
        prev_coords = coords
        
        
        # TODO: Keskikohat jossa diff lähellä nollaa
        # Filtteröi?
        # Lähellä nollaa ykkösiksi muut nolliksi
        # Yhdellä eteenpäin siftattu miinus alkuperäinen = nousut 1, laskut -1 (ei ole tarvetta)
        # Looppaa ekasta noususta seursaavaan laskuun laske keskikohta
        # Determine if this frame is good or bad for calibration
#        if diff < 0.02:
#            good_frames = np.append(good_frames, idx)
#        else:
#            bad_frames = np.append(bad_frames, idx)
        
        
    
    # Find smallest change periods
    
    b, a = scipy.signal.butter(3, 0.1, 'lowpass')
    diffs = scipy.signal.filtfilt(b, a, diffs)
    # Pick middle idxs
#    good_frames = 0
    return diffs[1:]

# TODO
# Check whether all points exists in MoCap data for this frame
def checker_points_exists():
    return False

# TODO
# Is this frame good for calibration based on MoCap data
def is_good_frame(coords):
    return False