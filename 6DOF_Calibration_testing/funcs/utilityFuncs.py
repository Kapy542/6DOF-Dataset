# -*- coding: utf-8 -*-

import csv
import os

# Write frame idx data in csv
# data: idx, idx_0, idx_1, real_idx_0, real_idx_1, timestamp_0, timestamp_1
def write_csv(data, path, name):       
    header = ['idx', 'idx_0', 'idx_1', 'real_idx_0', 'real_idx_1', 'timestamp_0', 'timestamp_1']
    path = os.path.join(path, name) + ".csv"
    print("\nWriting frame data to: " +  path)
    
    with open(path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
    
        # write the header
        writer.writerow(header)
    
        # write multiple rows
        writer.writerows(data)
    print("Success" + "\n")
        
# Write meta data in txt file
# data: {"Start": 0, "End": 0, "CropCoords_0": [0,0,0,0], "CropCoords_1": [0,0,0,0]} 
def write_meta(data, path, name):
    path = os.path.join(path, name) + ".meta"
    print("\nWriting meta data to: " +  path)
    with open(path, 'w') as outfile:
        outfile.write(repr(data))
    print("Success" + "\n")
    
# Read meta data from txt file
# data: {"Start": 0, "End": 0, "CropCoords_0": [0,0,0,0], "CropCoords_1": [0,0,0,0]} 
def read_meta(path, name):    
    path = os.path.join(path, name) + ".meta"
    print("\nReading meta data from: " +  path)
    
    f = open(path, 'r')
    d = f.read()
    d = d.replace('array', 'np.array')
    data = eval(d)
    print("Success" + "\n")
    return data