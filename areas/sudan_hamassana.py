# Settings of the original study in the Hamassana area (north east Sudan), kept so the first results can be repeated
# the data of this study was saved outside the project folder with its own file names

from areas.default import *


area_name = 'sudan_hamassana'

# the projection of the Hamassana data was not recorded, so the points are used as they are
area_epsg = None

# the data folder of the original study
dataDirectory = 'D:/Graduation/data'

# stack_file = os.path.join('Sentinel-2', 'Sentinel2_fullEL.tiff')
# stack_file = os.path.join('ASTER', 'ASTER_fullEL2.tiff')
# stack_file = os.path.join('Landsat-8', 'Landsat8_fullEL.tiff')
stack_file = os.path.join('Integration', 'RF_Integration.tiff')
# stack_file = os.path.join('Integration', 'Full_Integration.tiff')
sample_file = 'samples_point_exp.shp'
train_file = os.path.join('Geological', 'training.shp')
test_file = os.path.join('Geological', 'testing.shp')
output_folder = os.path.join('Integration', 'output_RFIN')

# the band names used in the original RF feature importance (25 bands), they must match the chosen stack_file
band_names = ['NE_Fualt', 'NW_Fualt', 'Lineament', 'Intrusion', 'PC4_Argillic', 'PC4_Phyllic', 'PC3_Propylitic',
              'PC4_OHbearing', 'PC2_IronOides', 'BR_2/1', 'BR_4/5', 'BR_4/6', 'BR_4/7', 'RBD1_Argillic', 'RBD2_Phyllic',
              'RBD3', 'RBD4', 'ALI', 'CLI', 'KAI', 'OHI', 'MNF1', 'MNF2', 'MNF3', 'MNF4']
