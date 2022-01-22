#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 11:27:36 2022

@author: varunkapoor
"""
from tifffile import imread
import pandas as pd
from scipy.ndimage import  median_filter
from skimage.morphology import skeletonize
from skimage.measure import regionprops
import os
from skimage.segmentation import find_boundaries
import matplotlib.pyplot as plt
from matplotlib import cm

def kymo_mtrack_export(fname, savedir, median_radius = 2):
    
    image = imread(fname)
    Name = os.path.basename(os.path.splitext(fname)[0])
    #Apply median filter to smooth the image
    median_image = median_filter(image, size = median_radius)
    #Apply sobel to get the edge image
    edge_image = find_boundaries(median_image)
    #Create a pixel level thich binary image
    skeleton_image = skeletonize(edge_image)
    #Use region props for getting the properties of the binary image
    properties = regionprops(skeleton_image)
    #Kymograph contains length vs time
    coordinates_lt = [prop.coords for prop in properties]
    #Sort the coordinates by time
    coordinates_lt = sorted(coordinates_lt, key=lambda k: k[1])
    doubleplot(image, skeleton_image, 'original_kymograph', 'for_mtrack_export')    
    df = pd.dataframe(coordinates_lt, columns = ['Length', 'Time'])
    #Save the data as Mtrack readable text file
    df.to_csv(savedir + '/' + Name + 'Mtrack' +  '.csv')          
      
    
def doubleplot(imageA, imageB, titleA, titleB):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    ax = axes.ravel()
    ax[0].imshow(imageA, cmap=cm.Spectral)
    ax[0].set_title(titleA)
    
    ax[1].imshow(imageB, cmap=cm.Spectral)
    ax[1].set_title(titleB)
    
    plt.tight_layout()
    plt.show()   