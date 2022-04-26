import napari 

import numpy as np 

from skimage.io import imread

from cellpose import models 
import skimage 


img = imread('../data/nuclei_images/Experiment-347_s1.ome-1.tif')

model_nuc =  models.Cellpose(gpu=True, model_type='nuclei')

img_gauss = skimage.filters.gaussian(
    img[:, 1000:1500, 1000:1500], sigma=1)
# viewer = napari.Viewer()
# viewer.add_image(img[:, 1000:1500, 1000:1500])

fast_mode = True

print('started segmentation')

masks, _, _, _ = model_nuc.eval(
    img_gauss, 
    z_axis = 0, 
    diameter = 70,
    anisotropy = 3.2, 
    channels = [0, 0], 
    do_3D=True,
    # batch_size = 1, # try smaller batch size for memory 
    # flow_threshold=0, # The QC step throws out masks that produce flows which are substantially different from the network's predicted flows. This mask->flow computation takes some time.    https://github.com/MouseLand/cellpose/issues/119 
    # rescale = True, 
)

print('finished segmentation')

np.save('masks-test-out.npy', masks)

viewer = napari.Viewer()
# viewer.add_image(img)
viewer.add_image(img_gauss)
viewer.add_labels(masks)