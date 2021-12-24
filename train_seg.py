"""
This script trains the cell segmentation U-Net

"""
from pathlib import Path
import time
import os

from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
#import tensorflow as tf


# Hide GPU from visible devices
#tf.config.set_visible_devices([], 'GPU')

from script.utilities import cfg
from script.model import unet_seg
from script.data import trainGenerator_seg

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
    
config_location = 'data/config_2D.json'

# Check if the config file exists
if Path(config_location).is_file():
    _msg("Config JSON file exists")

# Load configuration:
cfg.load_config(presets="2D", config_level="global", json_file=config_location)

# Files:
training_set = cfg.training_set_seg
print(training_set)
savefile = "unet_seg.hdf5" #cfg.model_file_seg

# Training parameters:
batch_size = 1
epochs = 300
steps_per_epoch = 1
patience = 50

# Data generator parameters:
data_gen_args = dict(
    rotation=2,
    rotations_90d=True,
    zoom=0.15,
    horizontal_flip=True,
    vertical_flip=True,
    illumination_voodoo=True,
    gaussian_noise=0.03,
    gaussian_blur=1,
)

# Generator init:
myGene = trainGenerator_seg(
    batch_size,
    os.path.join(training_set, "img"),
    os.path.join(training_set, "seg"),
    os.path.join(training_set, "wei"),
    augment_params=data_gen_args,
    target_size=cfg.target_size_seg,
    crop_windows=cfg.crop_windows,
)

# Define model:
model = unet_seg(input_size=cfg.target_size_seg + (1,))
model.summary()

# Callbacks:
model_checkpoint = ModelCheckpoint(
    savefile, monitor="loss", verbose=2, save_best_only=True
)
early_stopping = EarlyStopping(monitor="loss", mode="min", verbose=2, patience=patience)

# Train:
history = model.fit(
    myGene,
    steps_per_epoch=steps_per_epoch,
    epochs=epochs,
    callbacks=[model_checkpoint, early_stopping],
)
