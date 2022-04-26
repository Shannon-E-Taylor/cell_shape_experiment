import napari 
from skimage.io import imread
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import time 

import dask as da 

from numcodecs import Blosc # for zarr processing 

# initialize cle 
import pyclesperanto_prototype as cle
cle.select_device('RTX')

def process_masks(mask): 
    '''
    This scripts (will) takes as input 
    A mask of nuclei shape and position 
    And outputs the areas, xyz position, and diameters 
    doesn't work for images > VRAM 
    '''
    ###
    # remove small objects 
    start_time = time.time()
    mask = cle.exclude_small_labels(mask, maximum_size = 5000)
    print("removig small objects using clEsperanto took " + str(time.time() - start_time) + " s")
    mask = cle.exclude_labels_on_edges(mask)
    print("removig object on edge using clEsperanto took " + str(time.time() - start_time) + " s")

    
    # get dictionary of measurements
    stats = cle.statistics_of_labelled_pixels(None, mask)

    print("Determining label statistics using clEsperanto took " + str(time.time() - start_time) + " s")
    # read out arrays of values
    area = stats['area']
    mean = stats['mean_intensity']
    std_dev = stats['standard_deviation_intensity']
    centroids = stats['centroid']

    return(stats)



def process_masks(path): 
    mask = da.imread(path)
    masses = mask.ndmeasure.center_of_mass()


mask = np.load('../output/nuclear_segs/Experiment-347_s2.ome-1.tif/0.npy')
# mask = mask.astype(np.int16) 

process_masks(mask)

# #compress AND change the numpy array into a zarr array
# compressor = Blosc(cname='zstd', clevel=3, shuffle=Blosc.BITSHUFFLE)

# # Convert image into zarr array
# chunk_size = (100, 100)
# zarray = zarr.array(image, chunks=chunk_size, compressor=compressor)

# # save zarr to disk
# zarr_filename = '../../data/P1_H_C3H_M004_17-cropped.zarr'
# zarr.convenience.save(zarr_filename, zarray)
