import dask.array as da
import os 
from skimage.io import imread

files = os.listdir('../data/nuclei_images/')


for file in files: 
    if file not in os.listdir('../output/nuclear_segs/'): 
        img = imread('../data/nuclei_images/' + file)
        print('image loaded ' + file)
        image = np.moveaxis(np.array([img]), 0, 3) # function requires a numpy array, (z, y, x, channel)
        image = da.asarray(image)
        image = image.rechunk(chunks = (-1, 1000, 1000, -1))  # chunk z axis and color channel together 
        depth = tuple(np.ceil(diameter).astype(np.int64))
        boundary = "reflect"
        image.chunks
        # No chunking in channel direction
        image = da.overlap.overlap(image, depth + (0,), boundary)

        image.chunks