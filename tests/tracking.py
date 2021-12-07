"""
This script runs the tracking U-Net on data out of the segmentation U-Net.
Please make sure you have run the segmentation script first.

Images are processed in batches of 512, although the number of actual samples
run through the tracking U-Net will depend on the number of cells in each
image.

Format of images needs to be Position-Number-Chamber-Number-Frame-Number.fext
or Position-Number-Frame-Number.fext

If there are chambers, then it is assumed to be run in the mothermachine.
If there are no chambers, then images will be cropped as done for DeLTA 2D
@author: jblugagne
"""

import os
import glob

from delta.utilities import cfg
from delta.data import saveResult_track, predictCompilefromseg_track
from delta.model import unet_track

# Load config:
cfg.load_config(presets="2D")

# Input image sequences (change to whatever images sequence you want to evaluate):
inputs_folder = cfg.eval_movie
segmentation_folder = os.path.join(inputs_folder, "segmentation")

# Output folder:
outputs_folder = os.path.join(inputs_folder, "tracking")
if not os.path.exists(outputs_folder):
    os.makedirs(outputs_folder)

# List files to read
unprocessed = sorted(
    glob.glob(inputs_folder + "/*.tif") + glob.glob(inputs_folder + "/*.png")
)

# Load up model:
model = unet_track(input_size=cfg.target_size_track + (4,))
model.load_weights(cfg.model_file_track)

# Process
while unprocessed:
    # Pop out filenames
    ps = min(512, len(unprocessed))
    to_process = unprocessed[0:ps]
    del unprocessed[0:ps]

    # Get data:
    inputs, seg_filenames, boxes = predictCompilefromseg_track(
        inputs_folder,
        segmentation_folder,
        files_list=to_process,
        target_size=cfg.target_size_track,
        crop=cfg.crop_windows,
    )

    # Predict:
    results = model.predict(inputs, verbose=1)

    # Save (use the filenames list from the data compiler)
    saveResult_track(outputs_folder, results, files_list=seg_filenames)
