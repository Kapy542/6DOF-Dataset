#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2

# Create blob detector with specified settings
def create_detector():
    
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
    
    # Change thresholds
    params.minThreshold = 100
    params.maxThreshold = 255
    
    # Blobs are white so set to 255
    params.filterByColor = True
    params.blobColor = 255
    
    # Filter by Area. 
    # TODO: Check optimal values
    params.filterByArea = True
    params.minArea = 10
    params.maxArea = 100
    
    # Filter by Circularity 
    # TODO: Check optimal values
    params.filterByCircularity = True
    params.minCircularity = 0.6 # 0.8
    
    # Filter by Convexity
    # TODO: Check optimal values
    params.filterByConvexity = True
    params.minConvexity = 0.9 # 0.9
    
    # Filter by Inertia
    # TODO: Could be as strict as possible to filter out frames with motion blur
    # Now when testing with handheld checker, don't use
    params.filterByInertia = True
    params.minInertiaRatio = 0.4
    
    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    
    return detector

# Run detector for img and return coordinates
def detect_points(img, detector):
    
    # Convert to grayscale (not necessary)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    # Detect blobs.
    key_points = detector.detect(gray)
    
    return key_points

# Draw points and their indx onto img
def draw_points(img, keypoints):
    img_with_points = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    idx = 0
    for keypoint in keypoints:
        coord = (int(keypoint.pt[0]), int(keypoint.pt[1]) )
        cv2.putText(img=img_with_points, text=str(idx), org=coord, fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 255, 0),thickness=1)
        idx += 1 
    return img_with_points

# Reorder points on checker to match with MoCap data
def order_checkerpoints(keypoints):
    coords = extract_2d(keypoints)
    coords = coords * np.array([[5,1]])
    xy_sum = np.sum(coords,axis=1)
    min_idxs = xy_sum.argsort()
    ordered_keypoints = [keypoints[i] for i in min_idxs]
#    coords = coords * np.array([[1,10]])
#    ordered_points = keypoints
    return ordered_keypoints

# Extract only 2d positions from keypoints
def extract_2d(keypoints):
    coords = np.array([[0, 0]])
    for keypoint in keypoints:
        coord = np.array([[int(keypoint.pt[0]), int(keypoint.pt[1]) ]])
        coords = np.append(coords, coord, axis=0)
    return coords[1:]
 
# Check if all checkerpoints are found
def checker_points_found(keypoints):
    if len(keypoints) < 35:
        return False
    elif len(keypoints) > 40:
        return False
    return True

# Is this frame good for calibration based on checker detection
def is_good_frame(keypoints):
    if not checker_points_found(keypoints):
        return False
    return True

# Remove outliers so that there are exactly 35 points left
# Use mean position of the points and pick 35 points that are closest to that
# Does not guarantee that all points are part of the checer
def remove_outliers(keypoints):
    coords = extract_2d(keypoints)
    
    # Pick 35 points that are closest to the mean
    mean = np.mean(coords, axis=0)
    dist = np.linalg.norm(coords - mean, axis=1)
    min_idxs = dist.argsort()[:35]
    new_keypoints = [keypoints[i] for i in min_idxs]
    return new_keypoints



# Calibrate 
def calibrate():
    return False
