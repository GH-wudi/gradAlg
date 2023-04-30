# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 11:45:03 2021
@author: wfh
"""

import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

from IO import *
from test.toEach import lonlat2imagexy


def normalization(a):
	return (a - np.min(a)) / (np.max(a) - np.min(a))


def standardization(data):
	mu = np.mean(data, axis=0)
	sigma = np.std(data, axis=0)
	return (data - mu) / sigma


def lonlat2DN(dataset, lon_list, lat_list):
	DN = []
	for i in range(len(lat_list)):
		row, col = lonlat2imagexy(dataset, lon_list[i], lat_list[i])
		radiation_value = dataset.ReadAsArray(row, col, 1, 1)

		DN.append(radiation_value[0][0][0])
		# DN.append(radiation_value[13][0][0])
	# DN = np.array(DN).astype(np.uint32)
	# DN = standardization(DN)
	return DN


#  模型


def my_model():
	model = tf.keras.models.Sequential([

		tf.keras.layers.Dense(20, activation='selu'),
		tf.keras.layers.Dense(16, activation='selu'),
		tf.keras.layers.Dense(8, activation='selu'),
		tf.keras.layers.Dropout(0.3),
		tf.keras.layers.Dense(1)
	])

	model.compile(optimizer='adam',
	              loss='mean_squared_error',
	              metrics=['accuracy'])
	return model


def read_data():
	sheet = pd.read_excel(io=excel_path, sheet_name=sheet_name, usecols=cols)
	data = np.array(sheet.values)
	chla, lon_list, lat_list = data[:, 0], data[:, 1], data[:, 2]
	return chla, lon_list, lat_list


if __name__ == '__main__':
	os.environ['PROJ_LIB'] = r'D:\Program Files\PostgreSQL\13\share\contrib\postgis-3.0\proj'
	excel_path = r'..\9.22BYD\2021.9.22result.xlsx'
	image_path = r'D:\Code\Al\jz\rpcortho_bydquyu_jz.tif'
	sheet_name = 'Chla'
	model_path = './model'
	cols = [4, 5, 6]

	# 读取数据
	sheet = pd.read_excel(io=excel_path, sheet_name=sheet_name, usecols=cols)
	data = np.array(sheet.values)
	chla, lon_list, lat_list = data[:, 0], data[:, 1], data[:, 2]

	dataset = gdal.Open(image_path)
	raster_count = dataset.RasterCount

	# 数据预处理
	DN = lonlat2DN(dataset, lon_list, lat_list)
	# print(DN)
	DN = np.array(DN)
	# chla = np.array(chla)
	# DN = standardization(DN)
	# chla = standardization(chla)
	# X = DN.reshape(-1, 1)
	# X_train, X_test, Y_train, Y_test = train_test_split(X, chla, test_size=0.3, random_state=2)

	
	# m = np.mean(X_train)
	# s = np.std(X_train)

	# X_test -= m
	# X_test /= s
	# # X_test = X_test.reshape(-1, 2)
	# # 训练模型
	# model = my_model()
	# history = model.fit(X_train, Y_train,
	#                     epochs=500,
	#                     validation_split=0.25,
	#                     batch_size=5
	#                     )
	# # 模型保存
	# model.save(model_path)
	# model.evaluate(X_test, Y_test)
	# y = model.predict(X_test)

	# acc = history.history['accuracy']
	# val_acc = history.history['val_accuracy']
	# loss = history.history['loss']
	# # val_loss = history.history['val_loss']
	# epochs = range(len(acc))

	# plt.plot(epochs, acc, 'b', label='Training accuracy')
	# plt.plot(epochs, val_acc, 'r', label='validation accuracy')
	# plt.title('Training and validation accuracy')
	# plt.legend(loc='lower right')
	# plt.figure()

	# plt.plot(epochs, loss, 'r', label='Training loss')
	# # plt.plot(epochs, val_loss, 'b', label='validation loss')
	# plt.title('Training  loss')
	# plt.legend()
	# plt.show()
