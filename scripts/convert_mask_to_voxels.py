
import vedo 
import numpy as np
import os
import open3d as o3d

def to_voxels(path): 
    pointcloud = o3d.io.read_point_cloud(path)
    if pointcloud.has_points(): 
        mesh = vedo.load(path)
        vol = mesh.binarize()
        np.save(path + '_.npy', vol.tonumpy())


 
cell_list = os.listdir('../output/cell_segs_limeseg/Img_1_segmentation2.0/')

print('started')

for cell in cell_list: 
    path = '../output/cell_segs_limeseg/Img_1_segmentation2.0/' + cell + '/T_1.ply'
    try: 
        to_voxels(path)
    except: 
        print(path)

print('done')