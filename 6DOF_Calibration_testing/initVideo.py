# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:56:18 2022

@author: kapyla
"""

import sys, getopt
import numpy as np
import cv2
from funcs.ImgReader import ImgReader
from funcs.utilityFuncs import write_csv, write_meta, read_meta
import argparse
import os
import pickle

take_path = "m:031112_2"
out_path = "b:Videos_without_sound"


# Start of take #N   
take_name = os.path.split(take_path)[-1]
subject_name = take_name.split("_")[0]
    
print()
print("Initializing take: ", take_path)

img_reader = ImgReader(take_path, crop = False, show_idx = True, show_box = True)

if len(img_reader.img_list_0) == 0:
    print("ERROR: no images in", take_path)
    #return
       
data = img_reader.idx_data
write_csv(data, out_path, take_name)

# Window setup
output_size = (img_reader.img.shape[1], img_reader.img.shape[0])
cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.resizeWindow('window', output_size)

# img_reader.step()
while True:
    img = img_reader.img
    cv2.imshow('window', img)
    key = cv2.waitKey(0)
    print("You pressed:", key)   
    if key == ord('q'):
        break
    else:
        img_reader.navigate(key)

meta_data = img_reader.meta_data
write_meta(meta_data, out_path, take_name)
a = read_meta(out_path, take_name)

cv2.destroyAllWindows()
print()
del img_reader
print("Success!")
print()
