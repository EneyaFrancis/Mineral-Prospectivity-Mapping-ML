# This file chooses the study area and builds the paths of its data and outputs.
# The settings of each area are in the areas folder (e.g. areas/malawi.py), so adding a new area only needs
# a new file there, and the other python codes within the same directory import the settings from here.

import os
import importlib


# the active study area, it is the name of a file in the areas folder
# it can also be chosen without changing the code by setting the STUDY_AREA environment variable
study_area = os.environ.get('STUDY_AREA', 'malawi')

# load the settings of the chosen area and make them available as variables of this file
area = importlib.import_module('areas.' + study_area)
globals().update({name: value for name, value in vars(area).items() if not name.startswith('_')})



# the folder of the area data, an area file can set its own dataDirectory if the data is saved in another place
if not hasattr(area, 'dataDirectory'):
    dataDirectory = os.path.join(dataRoot, area_name)

# the full paths used by the other codes
remote_sensing_data = os.path.join(dataDirectory, stack_file)
sampleData = os.path.join(dataDirectory, sample_file)
trainDirectory = os.path.join(dataDirectory, train_file)
testDirectory = os.path.join(dataDirectory, test_file)

# the folder where the prediction maps are saved, and the folder of the grid search statistics
outputDirectory = os.path.join(dataDirectory, output_folder)
statisticsDirectory = os.path.join(outputDirectory, 'sta')
