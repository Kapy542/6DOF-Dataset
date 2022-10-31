#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: Need to check sync between cams and optitrack
# TODO: FPS_MULT automatically from the img name and csv?
# TODO: Should value in stationary period be averaged
# TODO: Should good frame also include data from img (all dots found, calibration possible)?
# TODO: How to express corresponding frames between img/mocap (When read ignore other than matching?)
# TODO: Might be wiser to use next_frame - current_frame. Cam exposes like that. Probaply too small error to bother
# TODO: Automatic recognition of point order? 

import os
import numpy as np
import pandas  
import scipy.signal

FPS_MULT = 5
FIRST_FRAME_IN_MOCAP = 0

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
# Top left 1, belof that 2 etc
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
# Get all frames where checker is stationary
def get_stationary_frames(df):
    diffs = np.array([0])
    prev_coords = get_checker_coords(FIRST_FRAME_IN_MOCAP, df)
    prev_diff = 0
   
    # TODO: Where to start so in sync?
#    for idx in range(FPS_MULT, len(df), FPS_MULT): 2000
    for idx in range(FIRST_FRAME_IN_MOCAP, len(df), FPS_MULT):    
        
        coords = get_checker_coords(idx, df)
        
        # Sjip if data is missing
        if not data_exists(coords):
            diff = prev_diff
            diffs = np.append(diffs, diff)
            continue
           
        # Calculate absulute difference in position from previous frame      
        diff = np.abs( np.sum(prev_coords-coords) )
        diffs = np.append(diffs, diff)
        prev_coords = coords
        prev_diff = diff
        
    # Remove init value
    diffs = diffs[1:]
                   
    # Filter to remove noise
    # More importantly flattens the curve so that there is only one local min per stationary period
    b, a = scipy.signal.butter(3, 0.3, 'lowpass')
    smooth_diffs = scipy.signal.filtfilt(b, a, diffs)
    
    # Get those local mins
    local_mins = scipy.signal.argrelextrema(smooth_diffs, np.less)[0]
    vals_in_mins = diffs[local_mins]
    
    # Get those local mins
    local_maxs = scipy.signal.argrelextrema(smooth_diffs, np.greater)[0]
    vals_in_maxs = diffs[local_maxs]
    
    # Remove frames with no data
    
    # Parse so that best ones remaain (actually good mins)
    # Min value bigger than some threshold?
    # (mean(max)-mean(min)/2
    # Some clustering algorithm (remove outliers)
    
    # Remove dublicate positions
    # Look for similarity measures (2D -> 1D string?)
    # Euclidean distance?
    
    return diffs, smooth_diffs, local_mins, vals_in_mins, local_maxs, vals_in_maxs

# TODO: 
# If in multiple frames checker is in similiar position and orientation,
# remove ones with most movement
def get_original_frames():
    return False

# TODO
# Check whether all points exists in MoCap data for this frame
def checker_points_exists():
    return False

# TODO
# Get good frames for calibration based on MoCap data
def get_good_frames(coords):
    
    return False

# TODO
# Check if there is untracked markers (NaN values)
def data_exists(coords):
    no_nan = coords == coords
    if no_nan.all():
        return True
    return False