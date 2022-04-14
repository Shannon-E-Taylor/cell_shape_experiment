
from skimage.io import imread
from cellpose import models
from cellpose.contrib import distributed_segmentation
import os 
import numpy as np

import dask_image.imread



# def run_segmentation(file, path): 
#     img = dask_image.imread.imread(path + file)
#     print(img.shape)

#     masks, flows_stitched, styles_stitched, _ = model.eval(img, 
#                                                         channels=[0, 0],
#                                                         diameter=d,
#                                                         anisotropy=anisotropy,  
#                                                         resample = False, 
#                                                         do_3D=True, 
#                                                         tile = True,  
#                                                         min_size = 10000, 
#                                                         batch_size = 1
#                                                         ) 
#     np.save('../output/nuclear_segs/' + file, masks)


######
# Define parameters 
######  

# model = models.Cellpose(model_type='nuclei', gpu = False)

print('model loaded')

anisotropy = 3.2892183369975223 # read from microsocopy file 
d = 100 # from data and by experimentation 

files = os.listdir('../data/nuclei_images/')

print('running')

for file in files: 
    if file not in os.listdir('../output/'): 
        # img = dask_image.imread.imread(image = da.from_array(img))
        img = imread('../data/nuclei_images/' + file )
        print('image loaded')
        img = np.moveaxis(np.array([img]), 0, 3) # function requires a numpy array, (z, y, x, channel)
        print(img.shape)


import dask
import dask.array as da
import functools
import logging
import operator
diameter = [30, 100, 100] 

diameter_yx = diameter[1]
anisotropy = diameter[0] / diameter[1] 

image = da.from_array(img, chunks = ('100 MiB'))
print(image.numblocks)
image = image.rechunk({-1: -1}, block_size_limit = 2e5)  # color channel is chunked together
print(image.numblocks)

depth = tuple(np.ceil(diameter).astype(np.int64))
boundary = "reflect"

# No chunking in channel direction
image = da.overlap.overlap(image, depth + (0,), boundary)


block_iter = zip(
    np.ndindex(*image.numblocks),
    map(
        functools.partial(operator.getitem, image),
        da.core.slices_from_chunks(image.chunks),
    ),
)
