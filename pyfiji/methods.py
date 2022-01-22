#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 11:27:36 2022

@author: varunkapoor
"""
from tifffile import imread
import pandas as pd
from scipy.ndimage import sobel, median_filter
from skimage.morphology import skeletonize
from skimage.measure import regionprops
import os

def kymo_matrack_export(fname, savedir, median_radius = 2):
    
    image = imread(fname)
    Name = os.path.basename(os.path.splitext(fname)[0])
    #Apply median filter to smooth the image
    median_image = median_filter(image, size = median_radius)
    #Apply sobel to get the edge image
    edge_image = sobel(median_image)
    #Create a pixel level thich binary image
    skeleton_image = skeletonize(edge_image)
    #Use region props for getting the properties of the binary image
    properties = regionprops(skeleton_image)
    #Kymograph contains length vs time
    coordinates_lt = [prop.coords for prop in properties]
    #Sort the coordinates by time
    coordinates_lt = sorted(coordinates_lt, key=lambda k: k[1])
        
    df = pd.dataframe(coordinates_lt, columns = ['Length', 'Time'])
    #Save the data as Mtrack readable text file
    df.to_csv(savedir + '/' + Name + 'Mtrack' +  '.csv')          
      