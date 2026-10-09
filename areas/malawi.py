# Settings of the Malawi study area, the defaults are imported and only the Malawi differences are changed here

from areas.default import *


area_name = 'malawi'

# WGS 84 / UTM zone 36S (EPSG:32736) covers the whole of Malawi
area_epsg = 32736

# the stacked data used as feature predictors, choose one of them by removing the comment
# the file names are the expected names inside data/malawi, change them to match the saved files
# stack_file = os.path.join('Sentinel-2', 'Sentinel2_Malawi.tiff')
# stack_file = os.path.join('Landsat-8', 'Landsat8_Malawi.tiff')
# stack_file = os.path.join('ASTER', 'ASTER_Malawi.tiff')
# stack_file = os.path.join('Geophysics', 'Geophysics_Malawi.tiff')
stack_file = os.path.join('Integration', 'Full_Integration.tiff')

# fill in the names of the bands in the same order as they are stacked
band_names = []
