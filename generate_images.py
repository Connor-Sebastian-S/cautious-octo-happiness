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

from scipy import interpolate
import skimage.transform as trans

from typing import cast, Tuple, List, Dict, Union, Iterator, Generator, Any, Optional


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
 
def shift(
    image: utils.Image, vector: Tuple[float, float], order: int = 0
) -> utils.Image:
    """
    Image shifting function

    Parameters
    ----------
    image : 2D numpy array
        Input image.
    vector : tuple of floats
        Translation/shit vector.
    order : int, optional
        Interpolation order. The default is 0.

    Returns
    -------
    shifted : 2D numpy image
        Shifted image.

    """
    transform = trans.AffineTransform(translation=vector)
    shifted = trans.warp(image, transform, mode="edge", order=order)

    return shifted


def zoomshift(
    I: utils.Image, zoomlevel: float, shiftX: float, shiftY: float, order: int = 0
) -> utils.Image:
    """
    This function zooms and shifts images.

    Parameters
    ----------
    I : 2D numpy array
        input image.
    zoomlevel : float
        Additional zoom to apply to the image.
    shiftX : float
        X-axis shift to apply to the image, in pixels.
    shiftY : float
        Y-axis shift to apply to the image, in pixels.
    order : int, optional
        Interpolation order. The default is 0.

    Returns
    -------
    I : 2D numpy array
        Zoomed and shifted image of same size as input.

    """

    oldshape = I.shape
    I = trans.rescale(I, zoomlevel, mode="edge", multichannel=False, order=order)
    shiftX = shiftX * I.shape[0]
    shiftY = shiftY * I.shape[1]
    I = shift(I, (shiftY, shiftX), order=order)
    i0 = (
        round(I.shape[0] / 2 - oldshape[0] / 2),
        round(I.shape[1] / 2 - oldshape[1] / 2),
    )
    I = I[i0[0] : (i0[0] + oldshape[0]), i0[1] : (i0[1] + oldshape[1])]
    return I


def get_random_crop(image, seg, grey, crop_height, crop_width):

    max_x = image.shape[1] - crop_width
    max_y = image.shape[0] - crop_height

    x = np.random.randint(0, max_x)
    y = np.random.randint(0, max_y)
    
    print(x)
    print(y)

    img = image[y: y + crop_height, x: x + crop_width]
    seg = seg[y: y + crop_height, x: x + crop_width]
    gr = grey[y: y + crop_height, x: x + crop_width]
    
    
    # #gr = data.illumination_voodoo(gr)
    # #gr = trans.rotate(gr, np.random.rand() *  np.random.randint(0, 12), mode="edge")
    # gr = np.fliplr(gr)
    # gr = np.flipud(gr)
    # rot = random.randint(0, 3)
    # gr = trans.rotate(gr, rot * 90.0, mode="edge")
        
    # #seg = trans.rotate(seg, np.random.rand() *  np.random.randint(0, 12), mode="edge")
    # seg = np.fliplr(seg)
    # seg = np.flipud(seg)
    # seg = trans.rotate(seg, rot * 90.0, mode="edge")

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
    
    no_of_imgs = 200
    _c = 1
    for count, img in enumerate(img_files):
        
        for i in range(no_of_imgs):
            
            # Set absolute path to segmentation image and open it
            ip = Path.cwd().joinpath(Path(cfg.training_set_seg), 'img', img)
            w = cv2.imread(
                str(ip)
            )
            
            # Set absolute path to segmentation image and open it
            i_g = cv2.imread(
                str(ip),
                0
            )
            _msg("Opened image located at %s" % ip)
            
            sp = Path.cwd().joinpath(Path(cfg.training_set_seg), 'seg', img)
            s = cv2.imread(
                str(sp),
                0
            )
            _msg("Opened image located at %s" % sp)
            
            ip = Path.cwd().joinpath(Path(cfg.training_set_seg), 'img', str(_c) + '.png')
            sp = Path.cwd().joinpath(Path(cfg.training_set_seg), 'seg', str(_c) + '.png')
            
            crop_img, crop_seg = get_random_crop(w, s, i_g, 512, 512)
            
            print('a')
            
            
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
