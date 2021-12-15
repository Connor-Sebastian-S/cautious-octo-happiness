# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 18:21:41 2021

@author: conno
"""
from pathlib import Path
import time
import glob
import os

import cv2
import numpy as np
import skimage.io

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
            
config_location = 'data/config_2D.json'

# Check if the config file exists
if Path(config_location).is_file():
    _msg("Config JSON file exists")

# Load configuration:
utils.cfg.load_config(presets="2D", config_level="global", json_file=config_location)

# Create required segmentation folders if not exist
if Path(cfg.training_set_seg).is_dir():
    _msg("Seg folder exists")
else:
    p = Path(cfg.training_set_seg) 
    p.mkdir(parents=True, exist_ok=True)
    _msg("Seg folder created")

if Path(Path.joinpath(Path(cfg.training_set_seg), 'img')).is_dir():
    _msg("Seg/img folder exists")
else:
    p = Path(Path.joinpath(Path(cfg.training_set_seg), 'img'))
    p.mkdir(parents=True, exist_ok=True)
    _msg("Seg/img folder created")
    
if Path(Path.joinpath(Path(cfg.training_set_seg), 'seg')).is_dir():
    _msg("Seg/seg folder exists")
else:
    p = Path(Path.joinpath(Path(cfg.training_set_seg), 'seg'))
    p.mkdir(parents=True, exist_ok=True)
    _msg("Seg/seg folder created")
    
if Path(Path.joinpath(Path(cfg.training_set_seg), 'wei')).is_dir():
    _msg("Seg/wei folder exists")
else:
    p = Path(Path.joinpath(Path(cfg.training_set_seg), 'wei'))
    p.mkdir(parents=True, exist_ok=True)
    _msg("Seg/wei folder created")
        
#_msg("Before continuing please put all of your images in the 'img' folder inside the 'seg' folder, located at %s" % Path.joinpath(Path(cfg.training_set_seg), 'img'))

#input(_msg("Once you have done this please press Enter to Continue"))

p = str(Path.joinpath(Path(cfg.training_set_seg), 'img'))

img_files = [
    x
    for x in os.listdir(p)
    if os.path.splitext(x)[1].lower() in (".tif", ".tiff", '.png', '.jpg', '.jpeg')
]

_msg("Found %d images in the 'img' folder inside the 'seg' folder, located at %s" % (len(img_files), p,))

#_msg("Before continuing please put all of your segmentation images in the 'seg' folder inside the 'seg' folder, located at %s" % Path.joinpath(Path(cfg.training_set_seg), 'seg'))

#input(_msg("Once you have done this please press Enter to Continue"))

p = str(Path.joinpath(Path(cfg.training_set_seg),'seg'))
seg_files = [
    x
    for x in os.listdir(p)
    if os.path.splitext(x)[1].lower() in (".tif", ".tiff", '.png', '.jpg', '.jpeg')
]

_msg("Found %d images in the 'seg' folder inside the 'seg' folder, located at %s" % (len(seg_files), Path.joinpath(Path(cfg.training_set_seg), 'seg')),)

for count, seg in enumerate(seg_files):
    
    # Set absolute path to segmentation image and open it
    ip = Path.cwd().joinpath(Path(cfg.training_set_seg), 'seg', seg)
    w = cv2.imread(
        str(ip)
    )
    _msg("Opened segmentation image located at %s" % ip)
    
    # Build weight map from segmentation image
    w = data.seg_weights_2D(w)
    
    # Change colour to BGR
    w = cv2.cvtColor(w, cv2.COLOR_GRAY2BGR)
    
    # For every pixel that is [1,1,1] change it to white [255,255,255]
    w[np.all(w == (1, 1, 1), axis=-1)] = (255,255,255)
    
    # Set absolute path to weight image and save it
    sp = Path.cwd().joinpath(Path(cfg.training_set_seg), 'wei', str(count+1) + '.png')
    cv2.imwrite(
        str(sp), 
        w)
    _msg("Saved weight image located at %s" % sp)