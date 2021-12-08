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

import script.utilities as utils
import script.config as cfg
import script.pipeline as pipe

def _root_dir():
    return os.path.dirname(os.path.abspath(__file__))

def test_pipeline_tif_stack():

    # Load configuration:
    utils.cfg.load_config(presets="2D", config_level="global", json_file='data/config_2D.json')
    
    # 'Pretend' arguments were passed to the cmd line:
    sys.argv = [sys.argv[0]]
    sys.argv.append(os.path.join(_root_dir(), cfg.project_dir))
    sys.argv.append(os.path.join(_root_dir(), cfg.res_dir))

    # Init reader
    xpreader = utils.xpreader()

    # Init pipeline:
    xp = pipe.Pipeline(xpreader)

    xp.process(frames=None)

    # Testing position pickle save
    import tempfile
    with tempfile.TemporaryDirectory() as tempdirname:
        assert len(xp.positions) > 0
        pos = xp.positions[0]
        pos.save(filename=tempdirname + "position0", save_format=("pickle",))
        import copy
        old_pos = copy.deepcopy(pos)

        # Testing Position.clear
        pos.clear()
        for k in pos.__dict__.keys():
            if k not in pos._pickle_skip:
                assert getattr(pos, k) is None

        # Testing Position.load
        pos.load(tempdirname + "position0.pkl")
        for k in old_pos.__dict__.keys():
            if k not in pos._pickle_skip:
                assert getattr(old_pos, k) == getattr(pos, k)         
    
def build_plot(
        pos: None, 
        x: Tuple[str, ...] = ('frames'), 
        y: Tuple[str, ...] = ('length'), 
        x_label: Tuple[str, ...] = ('frame #'),
        y_label: Tuple[str, ...] = ('length (pixels) #')
        ) -> Dict[str, Any]:
    
    import matplotlib.pyplot as plt
    
    import matplotlib.cm as mplcm
    import matplotlib.colors as colors
    
    lineage = pos.rois[0].lineage
    
    NUM_COLORS = len(lineage.cells)
    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=NUM_COLORS-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle('color', [scalarMap.to_rgba(i) for i in range(NUM_COLORS)])

    for count, cell in enumerate(lineage.cells):
        
        ax.plot(
            cell[x], 
            cell[y], 
            label=count)
        plt.legend(loc="upper left")
                                                  
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
    
def pipeline_analysis():

    pos = pipe.load_position('data/evaluation/alpha/results/Position000000.pkl')
    
    reader = utils.xpreader('data/evaluation/alpha')
    
    pos = pipe.Position(
        position_nb = 0,
        reader = reader,
        models = utils.loadmodels(),
        drift_correction = cfg.drift_correction,
        crop_windows = cfg.crop_windows
        )
    
    pos.load('data/evaluation/alpha/results/Position000000.pkl')
        
# =============================================================================
#     build_plot(pos=pos, 
#                x=('frames'), 
#                y=('fluo1'), 
#                x_label=('frame #'), 
#                y_label=('fluo (mean)')
#                )
# =============================================================================
   
import tensorflow as tf
with tf.device('/cpu:0'): 
    test_pipeline_tif_stack()
#pipeline_analysis()