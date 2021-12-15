# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 21:49:40 2021

Reads the content of our pickle file and displays it.

@author: connor
"""

import os
import sys
import glob
import os
import re
import time
import sys
import importlib
from threading import Thread
from typing import cast, Tuple, List, Optional, Union, Any, Dict
from pathlib import Path
import glob
import numpy as np

import script.utilities as utils
import script.config as cfg
import script.pipeline as pipe

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

    print("%s - " % (time.ctime()) + string)
    

def view_lineage(pos: pipe.Position):
    """
    View details about cell lineage 

    Parameters
    ----------
    pos : Pipeline.Position
        Saved Position object, from pkl file

    Returns
    -------
    None.

    """
    for r in pos.rois:
        cells = r.lineage.cells
        print(len(cells))
        for x, c in enumerate (cells):
            # mother frames daughters edges area width length perimeter fluo%d
            
            np.set_printoptions(formatter={'float': '{: 0.2f}'.format})
            
            #_msg('Cell: {}, fluo = {}'.format(x, np.array(c["fluo1"], dtype=np.float32)))
            
            _msg('Cell: {}, area = {}'.format(x, np.array(c["area"], dtype=np.float32)))
            
            _msg('Cell: {}, length = {}'.format(x, np.array(c["length"], dtype=np.float32)))
            
            _msg('Cell: {}, width = {}'.format(x, np.array(c["width"], dtype=np.float32)))
            
            _msg('Cell: {}, frames = {}'.format(x, np.array(c["frames"], dtype=np.float32)))
            
            # Max fluo value is white, so 255
    
def load_pickles():
    """
    Loads all of the pickle files for current experiment into memory

    Parameters
    ----------
    None.

    Returns
    -------
    None.

    """
    
    # Check that the config file exists 
    try:
        Path.joinpath(Path().resolve(), 'data/config_2D.json').resolve(strict = True)
    except FileNotFoundError:
        _msg("Loaded config files not located")
    else:
        _msg("Loaded config files located")
        
        # Load configuration:
        utils.cfg.load_config(
            presets="2D", 
            config_level="global", 
            json_file='data/config_2D.json'
            )
        
        pickles = glob.glob(str(Path.joinpath(Path().resolve(), cfg.res_dir, '*.pkl')))
    
        for n, position_pkl in enumerate(pickles):
        
            pos = pipe.load_position(position_pkl)
            
            reader = utils.xpreader(cfg.project_dir)
            
            pos = pipe.Position(
                position_nb = 0,
                reader = reader,
                models = utils.loadmodels(),
                drift_correction = cfg.drift_correction,
                crop_windows = cfg.crop_windows
                )
            
            pos.load(position_pkl)
            
            _msg("Loaded pickle file at {} for project at {}".format(position_pkl, cfg.project_dir))
            
            view_lineage(pos)

load_pickles()