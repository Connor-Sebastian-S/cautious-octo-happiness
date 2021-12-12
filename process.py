# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 02:19:12 2021
   
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
Transfer the pickle file (happens in pipeline.py save())
->
Done, and loop
    
@author: connor
"""

import time

#import schedule

import job_tasks as job

def process_everything():
    """
    The entire process of an experiment is here

    Parameters
    ----------
    None.

    Returns
    -------
    None.

    """
    
    # Delete old experiment folder
    job.clean_image_folder()
    
    # Create new experiment folder
    job.create_experiment

    # Capture new images
    job.capture_images()

    # Format images (name, format, size, etc.)
    job.format_images()

    # Check data integrity and folder structure - final checks
    job.integrity_check()

    # Run the pipeline (finally!)
    job.run_job()
    
job.run_job()

# # Schedule the 'job() function every Friday at 14:00
# schedule.every().friday.at("14:00").do(process_everything)

# while True:
#     schedule.run_pending()
#     time.sleep(1)