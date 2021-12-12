# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 00:33:41 2021

Contains functions for various project setup tasks. 

Basically everything that controls our process is here.

This is the order this shit runs in :)
    
    Delete old experiment folder
    ->
    Create new experiment folder
    ->
    Capture new images
    ->
    Format images (name, format, size, etc.)
    ->
    Check data integrity and folder structure - final checks
    ->
    Run the pipeline (finally!)
    ->
    Transfer the pickle file
    ->
    Done, and loop
    
@author: connor
"""

import time
import os
import sys
from pathlib import Path

import numpy as np
import cv2

import script.utilities as utils
import script.config as cfg
import script.pipeline as pipe

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

def remove_tree(path):
    """
    Delete a folder, specified as 'path'

    Parameters
    ----------
    path : str
        Directory path to remove.

    Returns
    -------
    None.

    """
    path = Path(path)
    for child in path.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            remove_tree(child)
    path.rmdir()
    
def clean_image_folder():
    """
    Delete the project folder - not needed at the end of the day

    Parameters
    ----------
    None.

    Returns
    -------
    None.

    """
    
    # Check that the project directory exists 
    try:
        Path.joinpath(Path().resolve(), _root_dir(), cfg.project_dir).resolve(strict = True)
    except FileNotFoundError:
        _msg("Project directory not located")
    else:
        _msg("Project directory files located")
        
        proj_directory = str(Path.joinpath(_root_dir(), cfg.project_dir))
        remove_tree(proj_directory)
    
def run_job():
    """
    Load config JSON and run pipeline

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
        
        # 'Pretend' arguments were passed to the cmd line:
        sys.argv = [sys.argv[0]]
        
        # Check that the project directory exists
        try:
            Path.joinpath(Path().resolve(), _root_dir(), cfg.project_dir).resolve(strict = True)
        except FileNotFoundError:
            _msg("Project directory not located")
        else:
            _msg("Project directory files located")
            sys.argv.append(str(Path.joinpath(Path().resolve(), _root_dir(), cfg.project_dir)))
           
        # Check that the results directory exists
        try:
            Path.joinpath(Path().resolve(), _root_dir(), cfg.res_dir).resolve(strict = True)
        except FileNotFoundError:
            _msg("Results directory not located")
        else:
            _msg("Results directory files located")
            sys.argv.append(str(Path.joinpath(Path().resolve(), _root_dir(), cfg.res_dir)))
            _msg("Project paths defined")
            
            # Initiate reader
            xpreader = utils.xpreader()

            # Initiate pipeline:
            xp = pipe.Pipeline(xpreader)

            # Process pipeline
            xp.process()
            
            _msg("Data processed")


def create_experiment():
    """
    Create our experiment folder, created using values in JSON file.
    Is run before image capture.
    
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
        
        # Check that the project directory doesn't exist

        _msg("Project directory not located")
        print(Path(Path.joinpath(Path().resolve(), _root_dir(), cfg.project_dir)))
        Path(Path.joinpath(Path().resolve(), _root_dir(), cfg.project_dir)).mkdir(parents=True, exist_ok=True)
        Path(Path.joinpath(Path().resolve(), _root_dir(), cfg.res_dir)).mkdir(parents=True, exist_ok=True)
        _msg("Project directory created")

 
def integrity_check():
    """
    Check images are correctly formatted, that the folder structure is correct, 
    and that all necessary scripts and hardware are functioning.
    
    Parameters
    ----------
    None.
    
    Returns
    -------
    None.
    
    """  
        
def capture_images():
    """
    Captures our images. Nothing more.
    
    Parameters
    ----------
    None.
    
    Returns
    -------
    None.
    
    """  
    
def format_images():
    """
    Converts images in a folder to jpeg for performance reasons in the pipeline.
    Ensures that the images all follow the same naming pattern, the order that 
    they are ordered in is based on creation time.
    
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

def image_similarity(img1: np.array, img2: np.array):
    """
    Converts images in a folder to jpeg for performance reasons in the pipeline.
    Ensures that the images all follow the same naming pattern, the order that 
    they are ordered in is based on creation time.
    
    Parameters
    ----------
    img1 : np.array
        Image 1 as numpy array
    img2 : np.array
        Image 2 as numpy array
    
    Returns
    -------
    is_same : boolean
        Whether images are the same (above lower threshold t)
    
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
    
    # Convert image 1 and image 2 to appropriate colour scheme
    #img1_grey = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    #img2_grey = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Calculate the histogram and normalize it
    img1_histogram = cv2.calcHist([img1], [0,1], None, [180,256], [0,180,0,256])
    img1_histogram = cv2.normalize(img1_histogram, img1_histogram, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX);
    img2_histogram = cv2.calcHist([img2], [0,1], None, [180,256], [0,180,0,256])
    img2_histogram = cv2.normalize(img2_histogram, img2_histogram, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX);
    
    # Find the metric value - the higher the metric, the more accurate the match
    metric_val = cv2.compareHist(img1_histogram, img2_histogram, cv2.HISTCMP_INTERSECT)
    
    # Our minimum accepted threshold
    t = 1.3
    print(metric_val)
    _msg("Images have similarity metric of %f" % metric_val)
    
    # Check if metric_value is greater than our lower threshold
    if metric_val > t:
        return True
    else:
        return False
    
def data_transfer(pickle_file: str):
    """
    Sends the Pickle file to a GitHub repo, why? Because I can. 
    Not secure in any way but it's cool. 
    Should be called at the end of the pipeline when the pkl is created, this way
    we don't need to reload the config file or check that the pkl actually exists.
    
    Parameters
    ----------
    pickle_file : str
        Directory path to pickle file.
    
    Returns
    -------
    None.
    
    """ 
    
    # g = Github("username", "password")
    
    # repo = g.get_user().get_repo('my-repo')
    # all_files = []
    # contents = repo.get_contents("")
    # while contents:
    #     file_content = contents.pop(0)
    #     if file_content.type == "dir":
    #         contents.extend(repo.get_contents(file_content.path))
    #     else:
    #         file = file_content
    #         all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
    
    # with open(pickle_file, 'r') as file:
    #     content = file.read()
    
    # # Upload to github
    # git_prefix = 'folder1/'
    # git_file = git_prefix + 'file.txt'
    # if git_file in all_files:
    #     contents = repo.get_contents(git_file)
    #     repo.update_file(contents.path, "committing files", content, contents.sha, branch="master")
    #     print(git_file + ' UPDATED')
    # else:
    #     repo.create_file(git_file, "committing files", content, branch="master")
    #     print(git_file + ' CREATED')
    
    print("wowee pickle has been moved somewhere")
 