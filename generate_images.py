# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 15:49:21 2021

@author: conno
"""

from pathlib import Path
import time
import glob
import os

import cv2
import numpy as np
import random
import skimage.io
from shutil import copyfile

import script.utilities as utils
import script.config as cfg
import script.data as data

def _msg(string: str):
    """
    Print timestamped messages

    Parameters
    ----------
    string : str
        Message to print.

    Returns
    -------
    None.

    """

    print("%s, Log: %s" % (time.ctime(), string))
 
def get_random_crop(image, seg, crop_height, crop_width):

    max_x = image.shape[1] - crop_width
    max_y = image.shape[0] - crop_height

    x = np.random.randint(0, max_x)
    y = np.random.randint(0, max_y)

    img = image[y: y + crop_height, x: x + crop_width]
    seg = seg[y: y + crop_height, x: x + crop_width]

    return img, seg
  
do_it = True
    
config_location = 'data/config_2D.json'

# Check if the config file exists
if Path(config_location).is_file():
    _msg("Config JSON file exists")
    
# Load configuration:
utils.cfg.load_config(presets="2D", config_level="global", json_file=config_location)

if do_it:         
    p = str(Path.joinpath(Path(cfg.training_set_seg), 'img'))
    q = str(Path.joinpath(Path(cfg.training_set_seg), 'seg'))
    
    img_files = [
        x
        for x in os.listdir(p)
        if os.path.splitext(x)[1].lower() in (".tif", ".tiff", '.png', '.jpg', '.jpeg')
    ]
    
    seg_files = [
        x
        for x in os.listdir(q)
        if os.path.splitext(x)[1].lower() in (".tif", ".tiff", '.png', '.jpg', '.jpeg')
    ]
    
    no_of_imgs = 5
    _c = 1
    for count, img in enumerate(img_files):
        
        for i in range(no_of_imgs):
            
            # Set absolute path to segmentation image and open it
            ip = Path.cwd().joinpath(Path(cfg.training_set_seg), 'img', img)
            w = cv2.imread(
                str(ip)
            )
            _msg("Opened image located at %s" % ip)
            
            sp = Path.cwd().joinpath(Path(cfg.training_set_seg), 'seg', img)
            s = cv2.imread(
                str(sp)
            )
            _msg("Opened image located at %s" % sp)
            
            ip = Path.cwd().joinpath(Path(cfg.training_set_seg), 'img', str(_c) + '.png')
            sp = Path.cwd().joinpath(Path(cfg.training_set_seg), 'seg', str(_c) + '.png')
            
            crop_img, crop_seg = get_random_crop(w, s, 512, 512)
            
            cv2.imwrite(str(ip), crop_img)
            cv2.imwrite(str(sp), crop_seg)
            
            _c += 1



# Get training image files list:
image_name_arr = glob.glob(os.path.join(cfg.training_set_seg, 'img', "*.png"))

# Get training image files list:
seg_name_arr = glob.glob(os.path.join(cfg.training_set_seg, 'seg', "*.png"))

images_input = []

# Load in the images
for n, filepath in enumerate(image_name_arr):
    images_input.append(cv2.imread(filepath))
    
images_input = np.array(images_input)

# # How many images to generate?
# no_of_imgs = 1

# for i in range(no_of_imgs):
    
#     #select random image
#     l = np.random.randint(0, len(images_input)-1)   
    
#     ii = []
#     ii.append(images_input[l])
     
#     zoomV = np.random.randint(0.15, 0.5)
#     # Augmentation parameters:
#     data_gen_args_img = dict(
#         rotation=np.random.randint(2,50),
#         rotations_90d=False,
#         zoom=zoomV,
#         horizontal_flip=False,
#         vertical_flip=False,
#         illumination_voodoo=True,
#         gaussian_noise=np.random.randint(0.01, 0.3),
#         gaussian_blur=np.random.randint(1, 20),
#     )
    
    
#     p = data.data_augmentation(ii, data_gen_args_img)
        
#     for i, img in enumerate(p):
#         cv2.imwrite(os.path.join(cfg.training_set_seg, 'img', str(len(images_input) + i) + ".png"), img*255)
#         copyfile(
#             os.path.join(cfg.training_set_seg, 'seg', str(l) + ".png"), 
            
#             os.path.join(cfg.training_set_seg, 'seg', str(len(images_input) + i) + ".png")
#             )
#         # copyfile(
#         #     os.path.join(cfg.training_set_seg, 'wei', str(l) + ".jpg"), 
            
#         #     os.path.join(cfg.training_set_seg, 'wei', str(len(images_input) + i) + ".jpg")
#         #     )
 