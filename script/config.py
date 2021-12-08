 # -*- coding: utf-8 -*-
"""
Module for configuration files and configuration parameters

"""
import os as _os
import json as _json
from warnings import warn as _warn
from typing import Tuple, Optional

from . import __file__ as _delta_init  # Path to __init__ file

"install directory"
_LOADED = None
"Which config file was loaded"
# Parameters:
res_dir: str = ''
"Results directory"
project_dir: str = ''
"Project directory"
presets: str = ''
"Type of analysis: can be '2D' or your own custom name for presets"
models: Tuple[str, ...] = ()
"Which models will be run"
model_file_rois: str = ''
"Model file for ROIs segmentation"
model_file_seg: str = ''
"Model file for cell segmentation"
model_file_track: str = ''
"Model file for cell tracking"
target_size_rois: Tuple[int, int] = (0, 0)
"ROI U-Net target/input image size"
target_size_seg: Tuple[int, int] = (0, 0)
"segmentation U-Net target/input image size"
target_size_track: Tuple[int, int] = (0, 0)
"tracking U-Net target/input image size"
training_set_rois: str = ''
"Path to ROIs U-Net training set"
training_set_seg: str = ''
"Path to segmentation training set"
training_set_track: str = ''
"Path to tracking training set"
eval_movie: str = ''
"Path to evaluation movie / image sequence"
rotation_correction: bool = False
"Flag to try to automatically correct image rotation (for microfluidic devices)"
drift_correction: bool = False
"Flag to correct drift over time (for microfluidic devices / ROIs)"
crop_windows: bool = False
"Flag to crop input image into windows of size target_size_seg for segmentation, otherwise resize them"
min_roi_area: float = 0.0
"Minimum area of detected ROIs, in pixels. Can be set to 0. (N/A for 2D)"
whole_frame_drift: bool = False
"If correcting for drift, use the entire frame instead of the region above the chambers"
min_cell_area: float = 0.0
"Minimum area of detected cells, in pixels. Can be set to 0"
save_format: Tuple[str, ...] = ()
"Format to save output data to"
TF_CPP_MIN_LOG_LEVEL: str = ''
"Debugging messages level from Tensorflow ('0' = most verbose to '3' = not verbose)"
memory_growth_limit: Optional[float] = None
"""If running into OOM issues or having trouble with cuDNN loading, try setting 
memory_growth_limit to a value in MB: (eg 1024, 2048...)"""
pipeline_seg_batch: int = 0
"""If running into OOM issues during segmentation with the pipeline, try lowering 
this value. You can also try to increase it to improve speed"""
pipeline_track_batch: int = 0
"""If running into OOM issues during tracking with the pipeline, try lowering 
this value. You can also try to increase it to improve speed"""

"""
IMPORTANT: Do not change the default parameters below. Update the .json files instead if necessary.
"""

_DEFAULTS_2D = dict(
    res_dir="",
    project_dir="",
    presets="2D",  # Type of analysis. Can be '2D' or your own custom name for presets
    models=("segmentation", "tracking"),  # Which models will be run
    model_file_rois="",  # Model file for ROIs segmentation (None for 2D)
    model_file_seg="data/models/unet_agarpads_seg_optimized.hdf5",  # Model file for cell segmentation (placeholder)
    model_file_track="data/models/unet_agarpads_track_optimized.hdf5",  # Model file for cell tracking(placeholder)
    target_size_rois=(512, 512),  # ROI U-Net target/input image size
    target_size_seg=(512, 512),  # segmentation U-Net target/input image size
    target_size_track=(256, 256),  # tracking U-Net target/input image size
    training_set_rois="",  # Path to ROIs U-Net training set (None for 2D)
    training_set_seg="data/training/segmentation_set/",  # Path to segmentation training set (placeholder)
    training_set_track="data/training/segmentation_set/",  # Path to tracking training set (placeholder)
    eval_movie="data\evaluation\beta",  # Path to evaluation movie / image sequence
    rotation_correction=False,  # Flag to try to automatically correct image rotation (for microfluidic devices)
    drift_correction=False,  # Flag to correct drift over time (for microfluidic devices / ROIs)
    crop_windows=True,  # Flag to crop input image into windows of size target_size_seg for segmentation, otherwise resize them
    min_roi_area=500,  # Minimum area of detected ROIs, in pixels. Can be set to 0. (N/A for 2D)
    whole_frame_drift=False,  # If correcting for drift, use the entire frame instead of the region above the chambers
    min_cell_area=20,  # Minimum area of detected cells, in pixels. Can be set to 0
    save_format=("pickle", "legacy", "movie"),  # Format to save output data to.
    TF_CPP_MIN_LOG_LEVEL="2",  # Debugging messages level from Tensorflow ('0' = most verbose to '3' = not verbose)
    memory_growth_limit=1024,  # If running into OOM issues or having trouble with cuDNN loading, try setting memory_growth_limit to a value in MB: (eg 1024, 2048...)
    pipeline_seg_batch=32,  # If running into OOM issues during segmentation with the pipeline, try lowering this value. You can also try to increase it to improve speed
    pipeline_track_batch=32,  # If running into OOM issues during tracking with the pipeline, try lowering this value. You can also try to increase it to improve speed
)

def load_config(json_file: str = None, presets: str = "2D", config_level: str = None):

    if presets == "2D":
        defaults = _DEFAULTS_2D
    else:
        raise ValueError(
            """Valid default presets are '2D'..
            If you implemented very different presets, please provide
            a config file to load_config() directely
            """
        )

    if json_file is None:

        # Is there a local/user config file for this preset?
        _json_file = _os.path.expanduser(
            _os.path.join("~/data", "config_%s.json" % presets)
        )
        if _os.path.exists(_json_file) and (
            config_level is None or config_level == "local"
        ):
            json_file = _json_file

        if (
            json_file is None
            and _os.path.exists(_json_file)
            and (config_level is None or config_level == "global")
        ):
            json_file = _json_file

        # If no file was found, raise error:
        if json_file is None:
            raise ValueError(
                """Could not find a local or global config file for presets '%s'.
                Either use delta.assets.download_assets() or provide a json_file path
                """
                % presets
            )

    variables = _read_json(json_file)


    # Update config variables:
    globals().update(variables)

    global _LOADED
    _LOADED = json_file

    # Tensorflow technical parameters:
    # Debugging messages level from Tensorflow ('0' = most verbose to '3' = not verbose)
   # _os.environ["TF_CPP_MIN_LOG_LEVEL"] = TF_CPP_MIN_LOG_LEVEL
    #_os.environ["CUDA_VISIBLE_DEVICES"] = ""

    # # If running into OOM issues or having trouble with cuDNN loading, try setting
    # # memory_growth_limit to a value in MB: (eg 1024, 2048...)
    # if memory_growth_limit is not None:
    #     import tensorflow as tf
    #     gpus =  tf.config.experimental.list_physical_devices ("GPU")
    #     print("Adjusting GPU settings")
    #     if gpus:
    #         # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
    #         try:
    #             print(gpus[0])
    #             tf.config.experimental.set_virtual_device_configuration(
    #                 gpus[0],
    #                 [
    #                     tf.config.experimental.VirtualDeviceConfiguration(
    #                         memory_limit=memory_growth_limit
    #                     ),
    #                 ],
    #             )
    #         except RuntimeError as e:
    #             # Virtual devices must be set before GPUs have been initialized
    #             print(e)
    
    # import tensorflow as tf
    # with tf.device('/cpu:0'):
    #     my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
    #     tf.config.experimental.set_visible_devices(devices= my_devices, device_type='CPU')

def _read_json(json_file: str):

    # Load file:
    print("Loading configuration from: %s" % json_file)
    with open(json_file, "r") as f:
        variables = _json.loads(f.read())

    # Type cast:
    for k, v in variables.items():
        if isinstance(v, list):
            variables[k] = tuple(v)  # Always use tuples, not lists in config

    return variables
