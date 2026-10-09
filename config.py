# This file chooses the study area and builds the paths of its data and outputs.
# The settings of each area are in the areas folder (e.g. areas/malawi.py), so adding a new area only needs
# a new file there, and the other python codes within the same directory import the settings from here.

import os
import importlib


# the active study area, it is the name of a file in the areas folder (malawi_south, malawi, sudan_hamassana)
# it can also be chosen without changing the code by setting the STUDY_AREA environment variable
study_area = os.environ.get('STUDY_AREA', 'malawi_south')

# load the settings of the chosen area
try:
    _area = importlib.import_module('areas.' + study_area)
except ModuleNotFoundError:
    raise ValueError('the study area {} has no settings file, add areas/{}.py'.format(study_area, study_area))

# the settings used by the other codes, a new setting added to areas/default.py must also be added here
area_name = _area.area_name
area_epsg = _area.area_epsg
area_boundary = _area.area_boundary
area_extent = _area.area_extent
band_names = _area.band_names
trainPercent = _area.trainPercent
random_seed = _area.random_seed
use_scaling = _area.use_scaling



# the folder of the area data, an area file can set its own dataDirectory if the data is saved in another place
dataDirectory = getattr(_area, 'dataDirectory', os.path.join(_area.dataRoot, area_name))

# the full paths used by the other codes
remote_sensing_data = os.path.join(dataDirectory, _area.stack_file)
sampleData = os.path.join(dataDirectory, _area.sample_file)
trainDirectory = os.path.join(dataDirectory, _area.train_file)
testDirectory = os.path.join(dataDirectory, _area.test_file)
boundaryDirectory = os.path.join(dataDirectory, area_boundary) if area_boundary is not None else None

# the folder where the prediction maps are saved, and the folder of the grid search statistics
outputDirectory = os.path.join(dataDirectory, _area.output_folder)
statisticsDirectory = os.path.join(outputDirectory, 'sta')
