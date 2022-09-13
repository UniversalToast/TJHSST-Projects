

import sys
import sklearn
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import metrics
mnist = fetch_openml('mnist_784', version=1)
mnist.keys()
data = mnist["data"]
target = mnist["target"]
data_train, data_test, target_train, target_test = data[:60000], data[60000:], target[:60000], target[60000:]
data_train = data_train[:10000]
target_train = target_train[:10000]
data_train = data_train/255.0
data_test = data_test/255.0
print("done1")

non_linear_model = SVC(kernel='rbf',decision_function_shape='ovr')
# linear_model = LinearSVC()
print("done2")
non_linear_model.fit(data_train, target_train)
print("done3")
target_pred = non_linear_model.predict(data_test)
print("accuracy:", metrics.accuracy_score(target_test, target_pred))
