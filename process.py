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
import os

import glob
import cv2
#import schedule

import job_tasks as job
import script.config as cfg

# def process_everything():
#     """
#     The entire process of an experiment is here

#     Parameters
#     ----------
#     None.

#     Returns
#     -------
#     None.

#     """
    
#     # Delete old experiment folder
#     job.clean_image_folder()
    
#     # Create new experiment folder
#     job.create_experiment

#     # Capture new images
#     job.capture_images()

#     # Format images (name, format, size, etc.)
#     job.format_images()

#     # Check data integrity and folder structure - final checks
#     job.integrity_check()

#     # Run the pipeline (finally!)
#     job.run_job()
    
# Get training image files list:
image_name_arr = glob.glob(os.path.join(cfg.evaluation_dir, "*.png"))

print(image_name_arr)

images_input = []

# Load in the images
for n, filepath in enumerate(image_name_arr):
    images_input.append(cv2.imread(filepath))
    
print (job.image_similarity(images_input[0], images_input[1]))

#job.create_experiment()
#job.run_job()



# # Schedule the 'job() function every Friday at 14:00
# schedule.every().friday.at("14:00").do(process_everything)

# while True:
#     schedule.run_pending()
#     time.sleep(1)