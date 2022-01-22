#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 11:27:36 2022

@author: varunkapoor
"""
from tifffile import imread, imwrite
import napari
import glob
import os
import numpy as np
from pathlib import Path
from qtpy.QtWidgets import QComboBox, QPushButton
import pandas as pd
from skimage.measure import label, regionprops

Boxname = 'Kymographs'
MTrack_label = '_MTrack_kymo'

class Mtrack_exporter(object):

    
    def __init__(self, viewer, imagename, Name, savedir, save = False, newimage = True):
     
          self.save = save
          self.newimage = newimage
          self.viewer = viewer
           
          print('reading image')      
          self.imagename = imagename  
          self.image = imread(imagename)
          self.Name = Name
          self.kymo_image = np.zeros(self.image.shape, dtype='uint16')
         
          print('image read')
          
            
          self.savedir = savedir
          
          
          self.kymo_create()
    def kymo_create(self):
                
                if self.save == True:
 
                        self.save_kymo_csv
                       
        
                if self.newimage == True:
                     for layer in list(self.viewer.layers):

                            self.viewer.layers.remove(layer) 
                    
                if self.save == False:
                        self.viewer.add_image(self.image, name = self.Name)
                        self.viewer.add_labels(self.kymo_image, name = self.Name + MTrack_label)

                      
    def save_kymo_csv(self):
            
        
         edge_image = label(self.kymo_image)
         largestCC = edge_image == np.argmax(np.bincount(edge_image.flat)[1:])+1
         largetslabel = np.max(largestCC)
         #Use region props for getting the properties of the binary image
         properties = regionprops(edge_image.astype('uint16'))
         #Kymograph contains length vs time
         coordinates_lt = []
         for prop in properties:
             if prop.label == largetslabel:
                 
                  coordinates_lt.append(prop.coords)
         coordinates_lt = np.asarray(coordinates_lt)         
         coordinates_lt = coordinates_lt[0]
         #Sort the coordinates by time
         coordinates_lt = sorted(coordinates_lt, key=lambda k: k[1])
         df = pd.DataFrame(coordinates_lt, columns = ['Length', 'Time'])
         #Save the data as Mtrack readable text file
         df.to_csv(self.savedir + '/' + self.Name + MTrack_label +  '.csv')
         imwrite(self.savedir + '/' + self.Name + MTrack_label + '.tif', self.kymo_image.astype('uint8'))


def export(sourcedir, savedir):

    Imageids = []
    Path(savedir).mkdir(exist_ok = True)
    
    
    
    Raw_path = os.path.join(sourcedir, '*tif')
    X = glob.glob(Raw_path)
    for imagename in X:
             Imageids.append(imagename)
    
    imageidbox = QComboBox()   
    imageidbox.addItem(Boxname)   
    tracksavebutton = QPushButton('Save Kymo_csv')
    
    for i in range(0, len(Imageids)):
    
    
         imageidbox.addItem(str(Imageids[i]))
            
            
    viewer = napari.Viewer()        
    viewer.window.add_dock_widget(imageidbox, name="Image", area='bottom')    
    viewer.window.add_dock_widget(tracksavebutton, name="Save Clicks", area='bottom')
    imageidbox.currentIndexChanged.connect(
             lambda trackid = imageidbox: Mtrack_exporter(
                     viewer,
                      imageidbox.currentText(),
                           os.path.basename(os.path.splitext(imageidbox.currentText())[0]), savedir, False, True ))     
    
    tracksavebutton.clicked.connect(
            lambda trackid= tracksavebutton:Mtrack_exporter(
                     viewer,
                      imageidbox.currentText(),
                           os.path.basename(os.path.splitext(imageidbox.currentText())[0]), savedir, True, False ))
     