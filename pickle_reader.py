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
    
    for r in pos.rois:
        cells = r.lineage.cells
        for c in cells:
            # mother frames daughters edges area width length perimeter fluo%d
            print(np.array(c["fluo1"], dtype=np.float32))
    
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
            
            _msg("Loaded pickle file at %s for project at %s" % (position_pkl, cfg.project_dir))
            
            view_lineage(pos)

load_pickles()