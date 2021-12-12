# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 15:57:27 2021

@author: conno
"""

import os
import sys

import script.utilities as utils
import script.config as cfg
import script.pipeline as pipe

def _root_dir():
    return os.path.dirname(os.path.abspath(__file__))

# running the pipeline passing cmd line arguments
def standard_img_file_formats():

    # Load configuration:
    utils.cfg.load_config(presets="2D", config_level="global", json_file='data/config_2D.json')
    
    # 'Pretend' arguments were passed to the cmd line:
    sys.argv = [sys.argv[0]]
    
    # Project directory and results directory are defined in config file!
    sys.argv.append(os.path.join(_root_dir(), cfg.project_dir))
    sys.argv.append(os.path.join(_root_dir(), cfg.res_dir))

    # Init reader
    xpreader = utils.xpreader()

    # Init pipeline:
    xp = pipe.Pipeline(xpreader)

    xp.process()

    
def bio_formats():   
    
    # Load configuration:
    utils.cfg.load_config(presets="2D", config_level="global", json_file='data/config_2D.json')
    
    # 'Pretend' arguments were passed to the cmd line:
    sys.argv = [sys.argv[0]]
    
    # Project directory and results directory are defined in config file!
    sys.argv.append(os.path.join(_root_dir(), cfg.project_dir))
    sys.argv.append(os.path.join(_root_dir(), cfg.res_dir))
    
    # Init reader
    xpreader = utils.xpreader(use_bioformats=True)
    
    # Init pipeline:
    xp = pipe.Pipeline(xpreader)
    
    xp.process() 
    
# '.tif', '.tiff', '.png', '.jpg', '.jpeg'

standard_img_file_formats()