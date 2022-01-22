#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 11:27:36 2022

@author: varunkapoor
"""
from tifffile import imread
import pandas
from scipy.ndimage import sobel
from skimage.morphology import skeletonize
from skimage.measure import regionprops

def kymo_matrack_export(fname, savedir, median_filter = 2):
    
    image = imread(fname)
    edge_image = sobel(image)
    skeleton_image = skeletonize(edge_image)
    props = regionprops(skeleton_image)
    for prop in props:
        
        coordinates_yx = prop.coords