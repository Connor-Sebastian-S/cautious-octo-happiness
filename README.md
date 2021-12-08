# cautious-octo-happiness

Temporary ReadMe until I can be bothered to write a proper one.

If you wish to setup an environment to run this application I recommend installing Anaconda, and then importing the PhD_env.yml file as a new environment.

Once that is done the application should be capable of running.

The file test_pipeline_tif.py is used for testing data, by default this test script uses the config.2D.json file for defining run settings. This file is located at data/config_2D.json.

Settings that are changeable in this file are:

"models": [
    "segmentation"
],

This defines which models to use. Choices are ["segmentation"] OR ["segmentation", "tracking"]. ["segmentation", "tracking"] requires multiple images to work.     

"res_dir": "data/evaluation/beta/results
Outpit directory for results files.

"project_dir": "data/evaluation/beta"
Directory containing input images. 

"rotation_correction": false
Whether to apply rotation correction to input images.

"drift_correction": false
Whether to apply drift correction to input images.

"min_cell_area": 10
Minimum area in pixels that a cell can be.

"save_format": [
    "pickle",
    "legacy",
    "movie"
]

Results output format. Pickle is a Python readable format, Legacy is a MATLAB compatible MAT file, and movie is a series of detailed images.

"TF_CPP_MIN_LOG_LEVEL": "3"
Tensorflow log level, 0 -> 3 = verbose -> less verbose

Setup for new images to test

By default you require a brightfield image, this is named "Position01Channel01Frames000001.jpg". The fluorescence image is called "Position01Channel02Frames000001.jpg" and is the same size as the brightfield one. The only difference between one and the other is the "Channel1" in the brightfield file name and the "Channel2" in the fluorescence image name - there can be as many fluorescence images as needed, though each must be the same name as their respective brightfield image except for an increment in the "Channelx" part of the filename. Note that fluorescence images are not necessary for the application to function. 

When the images are loaded the cells of interest are segmented in the brightfield image (Position01Channel01Frames000001.jpg) and this "mask" is used to determine where the cell is that frames corresponding fluorescence frame.

Filenames must follow this pattern: Position01Channel01Frames000001, incrementing Channel01 implies an additional fluorescence channel, incrementing Frames000001 implies an extra frame, and incrementing Position01 implies an extra camera position.

Ensure that "res_dir" and "project_dir" are coreectly setup in the config_2D.json file and point to your project folder relative to the test_pipeline_tif.py script, if this script is kept in the root folder of the application it will work as needed.

Run test_pipeline_tif.py, results are saved to the location defined by "res_dir".

I would recommend running the script without making any changes to the config file or the contents of the default test folder, just to ensure everything is setup correctly.