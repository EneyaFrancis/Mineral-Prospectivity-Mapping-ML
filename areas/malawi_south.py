# Settings of the southern region of Malawi, the Malawi settings are imported and only the differences are changed here
# the same data of the whole of Malawi is used, and the stack and the samples are cut to the southern region

from areas.malawi import *


area_name = 'malawi_south'

# the data folder of the whole of Malawi (data/malawi), so the data is not copied for the southern region
dataDirectory = os.path.join(dataRoot, 'malawi')

# an approximate rectangle around the Southern Region (Mangochi, Machinga, Zomba, Balaka, Neno, Mwanza, Blantyre,
# Chiradzulu, Thyolo, Mulanje, Phalombe, Chikwawa and Nsanje districts)
# a rectangle also covers small parts of the Central Region and Mozambique, so a boundary is better when available
area_extent = (34.2, -17.2, 36.0, -13.7)

# the exact boundary of the Southern Region, remove the comment when the shapefile is saved in data/malawi
# area_boundary = os.path.join('Boundaries', 'southern_region.shp')

# separate samples and outputs for the southern region, so the files of the whole of Malawi are not replaced
train_file = os.path.join('Samples', 'training_south.shp')
test_file = os.path.join('Samples', 'testing_south.shp')
output_folder = os.path.join('Output', 'south')
