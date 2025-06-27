# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 15:59:39 2025

@author: imageanalysis
"""

import tifffile
import numpy as np
import glob
import os 
import tkinter as tk 
from tkinter import filedialog


def read_tif_files(cycle=None):
    directory = filedialog.askdirectory(title = "Select Directory")
    
    if directory:
        if cycle:
            pattern = f"*{cycle}*.tif"
            
        else:
            pattern = "*tif"
        
    files = glob.glob(os.path.join(directory, pattern))
        
    all_pages = []
    
    for file in files:
        print(f"processin: {file}")
        try: 
            with tifffile.TiffFile(file) as tif:
                for page in tif.pages:
                    img = page.asarray()
                        
                    if img.dtype != np.uint16:
                        img = img.astype(np.uint16)
                        
                    all_pages.append(img)
                    
        except Exception as e:
            print(f"skipping {file} due to error : {e}")
    
    
    output_dir = filedialog.asksaveasfilename(title ='Save Directory',
                                                defaultextension = '.tif',
                                                filetypes =[("TIFF files", "*.tif"), ("All Files", "*.*")]
                                                )
    if all_pages:
        print(f"writing{len(all_pages)} pages to: {output_dir}")
        stacked = np.stack(all_pages, axis=0)
        tifffile.imwrite(output_dir, 
                      data = stacked, 
                      bigtiff = True, 
                      photometric = 'minisblack', 
                      compression = None)
            
    else:
        print("no images found to write")
            
    print(f"saved to :{output_dir}")
                


read_tif_files()









