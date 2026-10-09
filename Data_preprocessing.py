# This the basic code for remote sensing data preprocessing, where the stacked data is opened and prepared as feature
# predictors (x, x_test). the samples of ore deposit are processed as target variables (y, y_test)
# The code also contain how data is preprocessed to fit different ML models requirement.
# The code is mainly several function which can be called in others python codes within the same directory

from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from config import *
import tensorflow as tf
import numpy as np
import geopandas as gpd
import os
import random



driverTiff = gdal.GetDriverByName('GTiff')





# this function opens the stacked data, if the study area has a boundary or an extent in its settings
# the stack is cut to that area in memory (as VRT), so the original file is not changed
# all the functions which open the stacked data use it, so they all work on the same pixels
def open_stack(data):
    rs_ds = gdal.Open(data)
    if rs_ds is None:
        raise FileNotFoundError('the stacked data could not be opened: {}'.format(data))
    if area_boundary is not None:
        # the pixels outside the boundary are set to 0 (no data)
        rs_ds = gdal.Warp('', rs_ds, format='VRT', cutlineDSName=boundaryDirectory, cropToCutline=True, dstNodata=0)
    elif area_extent is not None:
        # the extent is in longitude and latitude (WGS 84)
        minx, miny, maxx, maxy = area_extent
        rs_ds = gdal.Translate('', rs_ds, format='VRT', projWin=[minx, maxy, maxx, miny], projWinSRS='EPSG:4326')
    return rs_ds



# this function for opening the stacked data to extract the x_train and x_test
# as well and reshaping the image to become as np array
# the nodata values of the bands are changed to NaN and then to 0, so empty pixels are always 0
def rs_preprocessing (data, reshape=True):
    rs_ds = open_stack(data)
    nbands = rs_ds.RasterCount
    band_data = []
    print('bands', rs_ds.RasterCount, 'rows', rs_ds.RasterYSize, 'columns',
          rs_ds.RasterXSize)
    if len(band_names) > 0 and len(band_names) != nbands:
        print('Warning: {} band names are given in the area settings but the stack has {} bands'.format(
            len(band_names), nbands))
    for i in range(1, nbands + 1):
        band = rs_ds.GetRasterBand(i).ReadAsArray().astype(np.float32)
        nodata = rs_ds.GetRasterBand(i).GetNoDataValue()
        if nodata is not None:
            band[band == nodata] = np.nan
        band_data.append(band)
    band_data = np.dstack(band_data)
    print(band_data.shape)

    if reshape == True:
        new_shape = (band_data.shape[0] * band_data.shape[1], band_data.shape[2])
        img_as_array = band_data[:, :, :int(band_data.shape[2])].reshape(new_shape)
        print('Reshaped from {o} to {n}'.format(o=band_data.shape, n=img_as_array.shape))
        img_as_array = np.nan_to_num(img_as_array)
        return band_data, img_as_array
    else:
        return band_data





# the next function accept shapefile data contains points as target variables samples
# the target value must be in attribute called value and values are binary (0,1)
# 1 represents that the target mineral exist and vice versa
# only the points inside the study area (area_boundary or area_extent in the area settings) are kept
# the points are reprojected to the projection of the study area (area_epsg in config.py) so they match the stacked data
# the function splits the data into train and test datasets and save them separately in two files

def target_variable (data, trainDirectory, testDirectory, tarinPercent=0.8):
    gdf = gpd.read_file(data)
    if gdf.crs is None:
        raise ValueError('the samples {} have no projection (.prj file), set it in QGIS first'.format(data))
    if area_boundary is not None:
        boundary = gpd.read_file(boundaryDirectory).to_crs(gdf.crs)
        gdf = gdf[gdf.within(boundary.union_all())]
    elif area_extent is not None:
        minx, miny, maxx, maxy = area_extent
        inside = gdf.to_crs(epsg=4326).cx[minx:maxx, miny:maxy].index
        gdf = gdf.loc[inside]
    if area_epsg is not None:
        gdf = gdf.to_crs(epsg=area_epsg)
    # def condition(dataframe):
    #     if dataframe['value'] == 1:
    #         value = 3
    #     elif dataframe['value'] == 0.5:
    #         value = 2
    #     else:
    #         value = 1
    #     return value
    # gdf['raster'] = gdf.apply(condition, axis=1)
    gdf['raster'] = np.where(gdf['Value'] == 0, 1, 2)
    print(gdf.head)
    print('samples inside the study area', gdf.shape[0], 'with the mineral', (gdf['Value'] == 1).sum(),
          'without the mineral', (gdf['Value'] == 0).sum())
    gdf_train = gdf.sample(frac=tarinPercent, random_state=random_seed)
    gdf_test = gdf.drop(gdf_train.index)
    print('gdf shape', gdf.shape, 'training', gdf_train.shape, 'test', gdf_test.shape)
    os.makedirs(os.path.dirname(trainDirectory), exist_ok=True)
    gdf_train.to_file(trainDirectory)
    gdf_test.to_file(testDirectory)
    print('train data saved to: {}'.format(trainDirectory))
    print('test data saved to: {}'.format(testDirectory))


# Data rasterization and extraction of training and testing dataset
# The folowing function accept
# (1) The RS data directory
# (2) The processed RS data
# (3) the directory of the training or testing dataset
# function return x (variable features) and y (target variables)
def dataFitting (RSData, band_data, SHfile):
    RS_ds = open_stack(RSData)
    train_ds = ogr.Open(SHfile)
    if train_ds is None:
        raise FileNotFoundError('the samples could not be opened: {}'.format(SHfile))
    lyr = train_ds.GetLayer()
    # the points and the stacked data must have the same projection, otherwise the points fall in the wrong pixels
    raster_srs = osr.SpatialReference(wkt=RS_ds.GetProjectionRef())
    if lyr.GetSpatialRef() is not None and not raster_srs.IsSame(lyr.GetSpatialRef()):
        print('Warning: the projection of {} is not the same as the stacked data'.format(SHfile))
    driver = gdal.GetDriverByName('MEM')
    target_ds = driver.Create('', RS_ds.RasterXSize, RS_ds.RasterYSize, 1, gdal.GDT_UInt16)
    target_ds.SetGeoTransform(RS_ds.GetGeoTransform())
    target_ds.SetProjection(RS_ds.GetProjectionRef())
    options = ['ATTRIBUTE=raster']
    gdal.RasterizeLayer(target_ds, [1], lyr, options=options)
    data = target_ds.GetRasterBand(1).ReadAsArray()
    print('min', data.min(), 'max', data.max(), 'mean', data.mean())
    truth = target_ds.GetRasterBand(1).ReadAsArray()
    classes = np.unique(truth)[1:]
    print('class values', classes)
    n_samples = (data > 0).sum()
    print('{n} training samples'.format(n=n_samples))
    if n_samples == 0:
        raise ValueError('no samples of {} fall inside the stacked data, check the projection and the study area'.format(SHfile))
    idx = np.nonzero(truth)
    x = np.nan_to_num(band_data[idx])
    y = truth[idx] - 1
    # def condition(dataframe):
    #     if dataframe == 3:
    #         value = 1
    #     elif dataframe == 2:
    #         value = 0.5
    #     else:
    #         value = 0
    #     return value
    # y = list(map(condition, truth[idx]))
    empty_samples = (x == 0).all(axis=1).sum()
    if empty_samples > 0:
        print('Warning: {} samples are on empty pixels (no data) of the stacked data'.format(empty_samples))
    print('Our X matrix is sized: {sz}'.format(sz=x.shape))
    print('Our y array is sized: {sz}'.format(sz=np.shape(y)))

    return x, y

# def get_map_prediction()



def tfPipline (feature, label, shuffle=True, repeat=False, BUFFER_SIZE=10000, BATCH_SIZE=64):
    if label == '':
        dataset = tf.data.Dataset.from_tensor_slices(feature)
    else:
        dataset = tf.data.Dataset.from_tensor_slices((feature, label))
    if repeat==True:
        dataset = dataset.repeat()
    if shuffle:
        dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
    else:
        dataset = dataset.batch(BATCH_SIZE)

    return dataset

def cnn_input(dataset):
    sample_size = dataset.shape[0]
    time_steps = dataset.shape[1]
    input_dimension = 1
    dataset = dataset.reshape(sample_size, time_steps, input_dimension)

    return dataset

def reset_random_seeds():
   os.environ['PYTHONHASHSEED']=str(random_seed)
   tf.random.set_seed(random_seed)
   np.random.seed(random_seed)
   random.seed(random_seed)


# the next function scales the features so all the bands have mean 0 and standard deviation 1
# the scaling is learned from the training data only, then the same scaling is applied to the other data
# it is needed for SVM, ANN and CNN when the bands have different units (e.g. magnetics and reflectance)
def scale_features(x_train, *others):
    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0)
    std[std == 0] = 1  # a band with one value only is not divided by 0
    return [(x_train - mean) / std] + [(data - mean) / std for data in others]


# the next function predicts all the pixels of the image
# if the RAM is not enough the image is predicted in slices and the slices are joined together
def predict_image(model, img_as_array):
    try:
        class_prediction = model.predict(img_as_array)
        print('Class prediction was successful without slicing!')
    except MemoryError:
        slices = int(round(len(img_as_array) / 2))
        while True:
            try:
                class_preds = list()
                for i in range(0, len(img_as_array), slices):
                    print('{} %, current: {}'.format((i * 100) / (len(img_as_array)), i))
                    class_preds.append(model.predict(img_as_array[i:i + slices]))
                class_prediction = np.concatenate(class_preds)
                break
            except MemoryError:
                slices = max(1, int(slices / 2))
                print('Not enought RAM, new slices = {}'.format(slices))
    return np.asarray(class_prediction).flatten()


# the next function creates the mask of the pixels which contain data (1) and the empty pixels (0)
# a pixel is empty when all its bands are no data (NaN) or 0, it works also for bands with negative values
def data_mask(band_data):
    mask = (np.nan_to_num(band_data) != 0).any(axis=2)
    return mask.astype(np.float32)


def write_raster(RSData, modelPrediction, band_data, savedDirectory):
    RS_ds = open_stack(RSData)
    cols = band_data.shape[1]
    rows = band_data.shape[0]
    modelPrediction = modelPrediction.astype(np.float32)  ##the same type as the saved raster (Float32)
    os.makedirs(os.path.dirname(savedDirectory), exist_ok=True)  ##creates the output folder if it does not exist
    driver = gdal.GetDriverByName("gtiff")
    outdata = driver.Create(savedDirectory, cols, rows, 1, gdal.GDT_Float32)
    outdata.SetGeoTransform(RS_ds.GetGeoTransform())  ##sets same geotransform as input
    outdata.SetProjection(RS_ds.GetProjection())  ##sets same projection as input
    outdata.GetRasterBand(1).WriteArray(modelPrediction)
    outdata.FlushCache()  ##saves to disk!!
    print('Image saved to: {}'.format(savedDirectory))

def main():
    print("This is the main code to test above functions")
    band_data1, img_as_array1 = rs_preprocessing(remote_sensing_data, reshape=True)
    x_train, y_train = dataFitting(remote_sensing_data, band_data1, trainDirectory)
    print(x_train)
    print(y_train)

if __name__ == '__main__':
    main()

