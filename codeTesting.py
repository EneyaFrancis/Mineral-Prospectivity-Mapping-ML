from Data_preprocessing import rs_preprocessing, dataFitting
from config import remote_sensing_data, trainDirectory

band_data1, img_as_array1 = rs_preprocessing(remote_sensing_data, reshape=True)

x_train, y_train = dataFitting(remote_sensing_data, band_data1, trainDirectory)
print(x_train)
print(y_train)
