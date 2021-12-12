# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 12:04:58 2021

@author: connor
"""

from __future__ import print_function

import os
import glob
import re
import random
import warnings
import copy
import importlib
from typing import cast, Tuple, List, Dict, Union, Iterator, Generator, Any, Optional

import cv2
import numpy as np
import numpy.typing as npt
import skimage.io as io
import tifffile
import skimage.transform as trans
from skimage.measure import label
import skimage.morphology as morph
from scipy import interpolate
from pathlib import Path
import glob

import script.data as data
import script.config as cfg

def _root_dir():
    """
    Returns the absolute path as a string

    Parameters
    ----------
    None.

    Returns
    -------
    string : str
        Absolute path.

    """
    return os.path.dirname(os.path.abspath(__file__))


def evaluation():
    """
    Evaluate the accuracy of segmentation

    Parameters
    ----------
    None.

    Returns
    -------
    None.

    """
    
    # Get training image files list:
    image_name_arr = glob.glob(os.path.join(cfg.evaluation_dir, "*.png"))
    
    print(image_name_arr)
    
    images_input = []

    # Load in the images
    for n, filepath in enumerate(image_name_arr):
        images_input.append(cv2.imread(filepath))
        
    images_input = np.array(images_input)
    
    # Augmentation parameters:
    data_gen_args = dict(
        rotation = 2,
        rotations_90d = True,
        zoom = 0.15,
        horizontal_flip = True,
        vertical_flip = True,
        illumination_voodoo = True,
        gaussian_noise = 50,
        gaussian_blur = 1
    )
    
    image_name_arr = data.data_augmentation(images_input, data_gen_args)
    
    for i, img in enumerate(image_name_arr):
        cv2.imwrite(os.path.join(cfg.evaluation_dir, str(i) + ".jpeg"), img*255)
    


evaluation()
    