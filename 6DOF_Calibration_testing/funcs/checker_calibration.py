#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2

# Create blob detector with specified settings
def create_detector():
    """
    Create
    """
    
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
    params.minCircularity = 0.8
    
    # Filter by Convexity
    # TODO: Check optimal values
    params.filterByConvexity = True
    params.minConvexity = 0.9
    
    # Filter by Inertia
    # TODO: Could be as strict as possible to filter out frames with motion blur
    # Now when testing with handheld checker, don't use
    params.filterByInertia = True
    params.minInertiaRatio = 0.1
    
    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    
    return detector

# Run detector for img and return coordinates
def detect_points(img, detector):
    
    # Convert to grayscale (not necessary)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    # Detect blobs.
    points = detector.detect(gray)
    
    return points

# Draw points and their indx onto img
def draw_points(img, keypoints):
    img_with_points = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    idx = 0
    for keypoint in keypoints:
        print(keypoint)
        coord = (int(keypoint.pt[0]), int(keypoint.pt[1]) )
#        cv2.putText(img=img_with_points, text=str(idx), org=(keypoint.pt[0], keypoint.pt[1]), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=1)
        cv2.putText(img=img_with_points, text=str(idx), org=coord, fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=1)
        idx += 1 
    return img_with_points

# Reorder points on checker to match with MoCap data
def order_checkerpoints(points):
    ordered_points = points
    return ordered_points
 
# Check if all checkerpoints are found
def checher_points_found():
    return False

# Is this frame good for calibration based on checker detection
def is_good_frame():