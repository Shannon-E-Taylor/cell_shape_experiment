"""Expand and reconstruct any surface
(here a simple box) into spherical harmonics"""
# Expand an arbitrary closed shape in spherical harmonics
# using SHTOOLS (https://shtools.oca.eu/shtools/)
# and then truncate the expansion to a specific lmax and
# reconstruct the projected points in red
import numpy as np
from scipy.interpolate import griddata
import pyshtools
from vedo import spher2cart, mag, Box, Point, Points, show, load

import open3d as o3d

import pandas as pd

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

import pymeshfix 


###########################################################################
lmax = 8              # maximum degree of the spherical harm. expansion
N    = 50             # number of grid intervals on the unit sphere
rmax = 200            # line length
###########################################################################

# path = '../output/cell_segs_limeseg/Img_1_segmentation1.0/Cell_4701/T_1.ply'

# pointcloud = o3d.io.read_point_cloud(path)

# x0 = np.array(pointcloud.get_center())
# # surface = Box(pos=x0+[10,20,30], size=(300,150,100)).color('grey').alpha(0.2)

# surface = load(path).color('grey').alpha(0.2)

############################################################



def run_harmonics(path, lmax, N, rmax): 
    pointcloud = o3d.io.read_point_cloud(path)
    if pointcloud.has_points(): 
        x0 = np.array(pointcloud.get_center())
        surface = load(path).color('grey').alpha(0.2)
    else: 
        print(path)
        return None


    agrid, pts = [], []
    for th in np.linspace(0, np.pi, N, endpoint=True):
        longs = []
        for ph in np.linspace(0, 2*np.pi, N, endpoint=False):
            p = spher2cart(rmax, th, ph)
            intersections = surface.intersectWithLine(x0, x0+p)
            if len(intersections):
                value = mag(intersections[0]-x0)
                longs.append(value)
                pts.append(intersections[0])
            else:
                # print('No hit for theta, phi =', th, ph)
                longs.append(rmax)
                pts.append(p)
        agrid.append(longs)
    agrid = np.array(agrid)

    #############################################################
    grid = pyshtools.SHGrid.from_array(agrid)
    clm = grid.expand()
    # These must be the components? 
    grid_reco = clm.expand(lmax=lmax).to_array()  # cut "high frequency" components

    return(grid_reco)


def make_watertight(path): 
    '''
    This code reads and cleans the existing mesh using the pymeshfix library
    There is a simpler command to achieve this : 
    pymeshfix.clean_from_file(infile, outfile)      
    But this crashes for me so I'm using the longer method from the docs 
    '''
    bpa_mesh = o3d.io.read_triangle_mesh(path)
    faces = np.asarray(bpa_mesh.triangles) 
    vertices = np.asarray(bpa_mesh.vertices) 

    # Create object from vertex and face arrays
    meshfix = pymeshfix.MeshFix(vertices, faces)
    # Repair input mesh
    meshfix.repair()
    # Save the mesh
    meshfix.save(path)

    

# results = pd.read_csv('../limeseg/near_noto_subset_2_out.csv')

# # filter results with a successful mesh 
# # and Euler characteristic of an enclosed object 
# results = results[
#     (results['Mesh ?'] == 'YES') & 
#     (results['Euler characteristic'] == 2)  & 
#     (results['Center Z'] > 40) & 
#     (results['Center Z'] < 100)
#     ]
# anisotropy = 0.25 / 0.0760332 

harmonics_list = []
import os 
cell_list = os.listdir('../output/cell_segs_limeseg/Img_1_segmentation1.0/')

print('got cell list')


for cell in cell_list[:200]: 
    path = '../output/cell_segs_limeseg/Img_1_segmentation1.0/' + cell + '/T_1.ply'
    # make_watertight(path)
    

    harmonics_list.append(run_harmonics(path, lmax, N, rmax))


print('ran SPHARM')

df = pd.DataFrame([i.flatten() for i in harmonics_list])
df['ID'] = 1

# get rid of all cells with tiny values 
# this may not be valid 
df.loc[~(abs(df) < 1e-10).all(axis=1)]

print(df.shape)

pca = PCA(0.95)

scaled_data = StandardScaler().fit_transform(df.drop(labels = ['ID'], axis = 1).dropna())

print(scaled_data)
principalComponents = pca.fit_transform(scaled_data)

principalDf = pd.DataFrame(data = principalComponents)

principalDf['ID'] = list(df['ID'])

print('did PCA')

print(principalDf)

fig, ax = plt.subplots(1, 2, figsize = (8, 3), tight_layout = True)

ax[0].scatter(principalDf.iloc[:, 0], principalDf.iloc[:, 1], c = 'k', alpha = 0.3)

ax[0].set_xlabel('PC1: ' + str(round(pca.explained_variance_ratio_[0] * 100)) + '%')

ax[0].set_ylabel('PC2: ' + str(round(pca.explained_variance_ratio_[1] * 100)) + '%')

ax[0].set_title('Blue: anterior. Red: posterior')


ax[1].scatter(principalDf.iloc[:, 0], principalDf.iloc[:, 2], c = 'k', alpha = 0.3)

ax[1].set_xlabel('PC1: ' + str(round(pca.explained_variance_ratio_[0] * 100)) + '%')

ax[1].set_ylabel('PC2: ' + str(round(pca.explained_variance_ratio_[2] * 100)) + '%')

ax[1].set_title('Blue: anterior. Red: posterior')


