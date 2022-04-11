
from skimage.io import imread
from cellpose import models
import os 
import numpy as np 



def run_segmentation(file, path): 
    img = imread(path + file)
    print(img.shape)

    masks, flows_stitched, styles_stitched, _ = model.eval(img, 
                                                        channels=[0, 0],
                                                        diameter=d,
                                                        anisotropy=anisotropy,  
                                                        resample = False, 
                                                        do_3D=True, 
                                                        tile = True,  
                                                        min_size = 10000, 
                                                        batch_size = 1
                                                        ) 
    np.save('../output/nuclear_segs/' + file, masks)


######
# Define parameters 
######  

model = models.Cellpose(model_type='nuclei', gpu = False)

print('model loaded')

anisotropy = 3.2892183369975223 # read from microsocopy file 
d = 100 # from data and by experimentation 

files = os.listdir('../data/nuclei_images/')

print('running')

for file in files: 
    if file not in os.listdir('../output/'): 
        run_segmentation(file, '../data/nuclei_images/')
        print('finished image 1')



