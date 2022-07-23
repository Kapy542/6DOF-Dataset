# -*- coding: utf-8 -*-

import numpy as np
import cv2
import glob
import os


class ImgReader:
    """
    Object that processes raw images. 
    Reads img_0, img_1 and combines them to wider img 
    
    path : str
        Path where .raw imgs are
    size_in : tuple
        Size of these imgs
    """
    
    def __init__(self, path, size = (1200,1920)):
        self.size = size
                            
        # Otherway around so "0" is on the left and "1" is on the right
        self.img_list_0 = sorted(glob.glob( os.path.join(path, "*_1_*.raw")  ) )
        self.img_list_1 = sorted(glob.glob( os.path.join(path, "*_0_*.raw")  ) )
        self.idx_data = np.empty([1,7]) # idx, idx_0, idx_1, real_idx_0, real_idx_1, timestamp_0, timestamp_1
        
        # Initialize black images
        self.img_0 = self.init_img()
        self.img_1 = self.init_img()
        self.padding =  np.zeros([size[0], 10, 3], dtype=np.uint8)
        self.img = self.join_imgs()
        
        # Keeps track of image index
        self.idx = 0
        self.meta_data = {"Start": 0, "End": -1} 
        
        self.imgs_left = True    # Helping when looping through images
        
        self.idx_listing() # Update idx_data
        self.init_stepping(self.meta_data)
        #try:
        #    self.update_imgs() # Update img_0, img_1 and img
        #except:
        #    pass
        
 
    
    ###################
    # Image functions #    
    ###################
    
    # Just generate black image
    def init_img(self):
        img = np.zeros([self.size[0], self.size[1], 3], dtype=np.uint8)
        return img
    
    # Converts raw bggr image to bgr. 
    # path: full image path [string]
    # img: bgr image [np.array]
    def read_img(self, path):
        file = open(path, "rb")
        img = np.fromfile(file, dtype=np.uint8)
        file.close()

        img = img.reshape( self.size )
        img = cv2.cvtColor(img, cv2.COLOR_BayerBG2BGR) # Raw images are bayer-bggr
        return img   

    # Join 2 images together with padding
    def join_imgs(self):
        img = np.append(self.img_0, self.padding, 1)
        img = np.append(img, self.img_1, 1)
        return img
    
    # Use idx and idx_data to update img, img_0 and img_1
    def update_imgs(self):
        idx_0 = self.idx_data[self.idx,1]
        idx_1 = self.idx_data[self.idx,2]
        
        image_0_path = self.img_list_0[idx_0]
        image_1_path = self.img_list_1[idx_1]   
        
        self.img_0 = self.read_img(image_0_path)
        self.img_1 = self.read_img(image_1_path)
        
        self.img = self.join_imgs()
        

    ######################
    # Indexing functions #
    ######################
    
    # Check if idx is in idx_data (in range)
    # idx: index we are looking for
    # exists: True/False
    def idx_exists(self, idx):
        exists = (0 <= idx < self.idx_data.shape[0])
        return exists
    
    # Set imgs to idx if it's in range
    # idx: new idx
    def set_idx(self, idx):
        if self.idx_exists(idx):
            self.idx = idx
            self.update_imgs()
            return 1
        else:
            return 0
            
    def init_stepping(self, meta_data):
        # If end frame is not defined:
        if meta_data["End"] == -1:
            meta_data["End"] = self.idx_data.shape[0]
        self.set_idx(self.meta_data["Start"])
        
    # Read next pair of images until we are on set END frame
    def step(self):
        self.set_idx(self.idx+1) # self.idx = self.idx+1
        self.imgs_left = (self.idx+1 < self.meta_data["End"]) # Do we have at least one more image
        
    # Extracts timestamp based index from image path
    # path: full image path [string]
    # idx: index of the image based on timestamp [int]
    def extract_timestamp_index(self, path):
        timestamp = float( path.split("_")[-2] ) / 1000 # to ms
        idx = int( round( timestamp / 50 ))            # 20 fps = 50 ms/img
        return idx
    
    # Extracts timestamp from image path
    # path: full image path [string]
    # timestamp: timestamp of the image [int]
    def extract_timestamp(self, path):
        timestamp = int( path.split("_")[-2] ) # us
        return timestamp
       
        
    # List all image idx's and corresponding idx's per camera
    # idx: Running index
    # idx_0: Index of the image that is used for corresponding idx
    # real_idx_0: Index that idx_0 corsseponds if it all images was there
    def idx_listing(self):
        if len(self.img_list_0) == 0:
            return
            
        self.idx = 0
        self.idx_0 = 0
        self.idx_1 = 0
        self.imgs_left = True
        
        # Define and ignore later
        data = np.empty([1,7]).astype(int)
        while self.imgs_left:
            image_0_path = self.img_list_0[self.idx_0]
            image_1_path = self.img_list_1[self.idx_1]   
            
            # Real index of the image based on timestamps (in case some images are missing)
            real_idx_0 = self.extract_timestamp_index(image_0_path)
            real_idx_1 = self.extract_timestamp_index(image_1_path)
            
            timestamp_0 = self.extract_timestamp(image_0_path)
            timestamp_1 = self.extract_timestamp(image_1_path)
            
            data = np.append(data, [[self.idx, self.idx_0, self.idx_1, real_idx_0, real_idx_1, timestamp_0, timestamp_1]], axis=0)
            
#            print(self.idx, real_idx_0, self.idx_0, real_idx_1, self.idx_1)
            
            # Update image if it's corresponding (otherwise use previous)
            if real_idx_0 == self.idx:
                self.idx_0 += 1
            if real_idx_1 == self.idx:
                self.idx_1 += 1   
                                
            self.idx += 1
            self.imgs_left = self.idx_0 < len(self.img_list_0) and self.idx_1 < len(self.img_list_1)
                    
        self.idx = 0
        self.idx_0 = 0
        self.idx_1 = 0
        self.imgs_left = True
        self.idx_data = data[1:] # Ignore first line



