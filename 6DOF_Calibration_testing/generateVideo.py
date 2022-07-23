# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 12:29:52 2021

@author: Kapyl
"""

#!/usr/bin/python

import sys, getopt
import numpy as np
import cv2
from funcs.ImgReader import ImgReader
import argparse
import os

take_path = "/home/kapyla/Desktop/KandiVol2/6DOF_Calibration_testing/CameraData/dotted_checker_1/"
out_path = "/home/kapyla/Desktop/KandiVol2/6DOF_Calibration_testing/out/" 
fps = 20

def main(take_path, out_path, visualize):
    
    take_name = os.path.split(take_path)[-1]
    subject_name = take_name.split("_")[0]
    out_dir = os.path.join(out_path, subject_name)
    try:
        os.mkdir(out_dir)
    except OSError as error:
        print(error)       
    video_path = os.path.join(out_dir, take_name) + ".mp4" # HOX
    #out_path = os.path.join(out_path, take_name) + ".avi" # HOX
    
    print()
    print("Trying to generate video from:", take_path)
    print("To:", out_path)
    
    img_reader = ImgReader(take_path)
    if len(img_reader.img_list_0) == 0:
        print("ERROR: no images in", take_path)
        return
       
    # Video writing setup
    output_size = (img_reader.img.shape[1], img_reader.img.shape[0])
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, output_size )
    #out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'XVID'), fps, output_size )
    
    # Window setup
    if visualize:
        cv2.namedWindow('window', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('window', output_size)
    
    idx=0
    # Loop through all images
    #while idx < 10:
    while img_reader.imgs_left:
        
        img_reader.step()
        
        img = img_reader.img
        out.write(img)
        #progress(img_reader.idx, len(img_reader.img_list_0), status='Doing very long job')
        
        if visualize:
            cv2.imshow("window", img)       
            # Press Q on keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break    
          
        idx += 1
        
    
    out.release()
    cv2.destroyAllWindows()
    print()
    del img_reader
    print("Success!")
    print()

main(take_path, out_path, True)