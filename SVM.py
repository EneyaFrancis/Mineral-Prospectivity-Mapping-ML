from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix, cohen_kappa_score, classification_report
from sklearn.svm import SVR
from Data_preprocessing import *
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import cross_val_score, GridSearchCV

from config import *


##the paths of the study area data (remote_sensing_data, trainDirectory, testDirectory) are defined in config.py

band_data, img_as_array = rs_preprocessing(remote_sensing_data, reshape=True)
x_train, y_train = dataFitting(remote_sensing_data, band_data, trainDirectory)
x_test, y_test = dataFitting(remote_sensing_data,band_data, testDirectory)

##scale the bands when use_scaling is True in the area settings (the scaling is learned from x_train only)
if use_scaling:
    x_train, x_test, img_as_array = scale_features(x_train, x_test, img_as_array)

reset_random_seeds()

svm = SVR(kernel='rbf')


# gamma = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
gamma = [0.75]
C = [0.1, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 10, 20, 25, 30, 40, 50, 75, 100]
# C = [1.5]
# C = [i : i for i in range (0.5, 50, 0.5)]
param_dictionary = dict(gamma=gamma, C=C)

grid = GridSearchCV(estimator=svm, param_grid=param_dictionary, scoring='neg_mean_squared_error', n_jobs=1, cv=5)
model = grid.fit(x_train, y_train)
print('best result', model.best_score_, 'from', model.best_params_)
df = pd.DataFrame(model.cv_results_)
# df.to_excel(os.path.join(statisticsDirectory, 'SVM_sta.xlsx'))

##SVR can predict values below 0 or above 1, so the predictions are kept between 0 and 1
y_predicted = np.clip(model.predict(x_test), 0, 1)
round_prediction = [round(i) for i in y_predicted]

print(y_predicted)
print(round_prediction)
print(y_test)

auc = roc_auc_score(y_test, y_predicted)
print(auc)
fpr, tpr, _ = roc_curve(y_test, y_predicted)
plt.plot(fpr,tpr, color ='red', lw=2, label="All Variables")
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([-.05, 1.0])
plt.ylim([-.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.show()

table = pd.DataFrame(confusion_matrix(y_test, round_prediction))
print(classification_report(y_test, round_prediction))
print('K = ', cohen_kappa_score(y_test, round_prediction))
plot = sns.heatmap(table, annot=True, fmt='d', cmap="Blues")
# plot = sns.heatmap(table, annot=True, cmap='viridis')
plt.show()

class_prediction = np.clip(predict_image(model, img_as_array), 0, 1)

class_prediction = class_prediction.reshape(band_data[:, :, 0].shape)
print('Reshaped back to {}'.format(class_prediction.shape))

mask = data_mask(band_data) # all actual pixels have a value of 1.0 and the empty pixels 0

class_prediction_ = class_prediction*mask

plt.subplot(121)
plt.imshow(class_prediction, cmap=plt.cm.Spectral)
plt.title('classification unmasked')

plt.subplot(122)
plt.imshow(class_prediction_, cmap=plt.cm.Spectral)
plt.title('classification masked')

plt.show()

output_image = os.path.join(outputDirectory, 'SVM_{}.tiff'.format(area_name))
write_raster(remote_sensing_data, class_prediction_, band_data, output_image)  ##the masked prediction is saved, the empty pixels are 0

del model