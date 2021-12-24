# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import json
import numpy as np
import matplotlib.pyplot as plt

import os

PATH = 'data/img/'
MASK_PATH = 'data/seg/'
RESULT_PATH = 'data/obj/'

f = []
for (dirpath, dirnames, filenames) in os.walk(PATH):
    f.extend(filenames)
    break
    
keys = []
ext = '.png'
for name in f:
    if(name.endswith(ext)):
        print(name)
        keys.append(name[0:len(name)-len(ext)])
    
if not os.path.exists(RESULT_PATH):
    os.makedirs(RESULT_PATH)
    
for key in keys:
    print(key)
    img = cv2.imread('{}{}.png'.format(PATH, key))
    mask = cv2.imread('{}{}.png'.format(MASK_PATH, '{}_seg'.format(key)))
    
    a, _, _ = cv2.split(mask)

    # Get image from mask
    mask_out = cv2.subtract(mask, img)
    mask_out = cv2.subtract(mask, mask_out)
    b_c, g_c, r_c = cv2.split(mask_out)
    mask_out = cv2.merge((b_c, g_c, r_c, a))

    ## get contours
    imgray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Get rect from contour
    index = 0
    for i in range(len(contours)):
        if (len(contours[i]) > len(contours[index])):
            index = i
    rect = cv2.boundingRect(contours[index])

    # Croop image
    cropped_img = mask_out[rect[1]:(rect[1]+rect[3]), rect[0]:(rect[0]+rect[2])]

#     blank_image = np.zeros((mask.shape[0],mask.shape[1],3), np.uint8)
#     cv2.drawContours(blank_image, contours, -1, (0,255,0), 3)

#     plt.imshow(blank_image)
#     plt.show()

#     plt.imshow(cropped_img)
#     plt.show()

    folder = None
    folder = 'cells/'
    
    if folder is not None and not os.path.exists('{}{}'.format(RESULT_PATH,folder)):
        os.makedirs('{}{}'.format(RESULT_PATH,folder))

    cv2.imwrite('{}{}{}.png'.format(RESULT_PATH, folder, key), cropped_img)
    print('image saved')