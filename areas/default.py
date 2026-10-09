# This file contains the default settings shared by all the study areas.
# Each study area has its own file in this folder which imports these defaults and changes only what is
# different for that area (e.g. the projection, the stacked data or the band names).

import os


# the name of the study area, it is used for the data folder and the names of the output maps
area_name = 'default'

# the main folder of all the data, each area has its own folder inside it (e.g. data/malawi)
dataRoot = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# the EPSG code of the projection used for the area, the sample points are reprojected to it
# None means the points are used as they are, without reprojection
area_epsg = None

# the part of the stacked data used for the study, the stack and the samples are cut to it
# area_boundary is a shapefile (polygon) inside the area folder, it gives the exact shape of the study area
# area_extent is a rectangle (min longitude, min latitude, max longitude, max latitude) in WGS 84
# the boundary is used if both are given, None means the whole stack is used
area_boundary = None
area_extent = None



# the files inside the area folder, the stacked data used as feature predictors and the samples of ore deposit
# the samples are points with an attribute called Value, 1 where the target mineral exists and 0 where it does not
stack_file = os.path.join('Integration', 'Full_Integration.tiff')
sample_file = os.path.join('Samples', 'samples_point.shp')
train_file = os.path.join('Samples', 'training.shp')
test_file = os.path.join('Samples', 'testing.shp')
output_folder = 'Output'

# names of the bands in the same order as they are stacked in the stack_file
# used to label the feature importance of the RF model, so the number of names must equal the number of bands
band_names = []

# the percentage of samples used for training, the rest is used for testing
trainPercent = 0.8

# scale the bands to the same range before training SVM, ANN and CNN
# needed when the stack mixes layers with different units (e.g. magnetics in nT and reflectance from 0 to 1)
use_scaling = True

# the seed of the random functions, so the code gives the same results every time it runs
random_seed = 1
