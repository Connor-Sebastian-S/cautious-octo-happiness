# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 09:24:30 2021

@author: conno
"""
import pandas as pd
import numpy as np
import os

import cv2

import matplotlib.pyplot as plt

from skimage.io import imread, imshow
from skimage.transform import resize

# Don't Show Warning Messages
import warnings
warnings.filterwarnings('ignore')


def overlay_transparent(src, overlay, x, y, overlay_size=None):

    src = src.copy()
    	
    if overlay_size is not None:
        overlay = cv2.resize(overlay.copy(), overlay_size)
       
       	# Extract the alpha mask of the RGBA image, convert to RGB 
    b,g,r,a = cv2.split(overlay)
    overlay_color = cv2.merge((b,g,r))
       	
    # Apply some simple filtering to remove edge noise
    #ksize = (10, 10)
    #mask = cv2.blur(a, ksize)
    
    mask = a
    
    
    
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
    #mask = cv2.morphologyEx(a, cv2.MORPH_OPEN, kernel, iterations=3)

       
    h, w, _ = overlay_color.shape
    roi = src[y:y+h, x:x+w] 
       
       	# Black-out the area behind the logo in our original ROI
    img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))

       	# Mask out the logo from the logo image.
    img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    img2_fg = cv2.morphologyEx(img2_fg, cv2.MORPH_OPEN, kernel, iterations=3)
       
       	# Update the original image with our new ROI
    src[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)
    
    return src

path = 'data/generation/data/background/background.png'

# read the image
bground = cv2.imread(path, cv2.IMREAD_UNCHANGED)
 
 #b_channel, g_channel, r_channel = cv2.split(bground)
 #alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 #creating a dummy alpha channel image.
# bground = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
 

max_x = 1600
max_y = 1200

bground = cv2.resize(bground, (1600, 1200))
 

for i in range(0,200):
    
    # cell_1 path
    cell_1 = cv2.imread('data/generation/data/obj/cells/1.png', cv2.IMREAD_UNCHANGED)
    
     # add a random rotation to the cell
    cell_1 = np.rot90(cell_1, k=np.random.randint(0,3))

     # get the shape after rotation
    shape = cell_1.shape
     #print(shape)
    
    # set the width and height
    h=shape[0]
    w=shape[1]
   
     # get a random x-coord
    y=np.random.randint(0, max_y-h)
     # get a random y-coord
    x=np.random.randint(0, max_x-w)
     
    
    bground = overlay_transparent(bground, cell_1, x, y)


image = np.flip(bground, axis=-1) 
cv2.imwrite('data/generation/data/results/test.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

