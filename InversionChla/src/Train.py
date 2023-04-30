# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 11:45:03 2021
@author: wfh
"""
import numpy as np
import os

import pandas as pd
import tensorflow as tf

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
		DN.append(radiation_value[6][0][0])
		DN.append(radiation_value[13][0][0])
	# DN = np.array(DN).astype(np.uint32)
	# DN = standardization(DN)
	return DN


def my_model():
	model = tf.keras.models.Sequential([

		tf.keras.layers.Dense(32, activation='selu'),
		tf.keras.layers.Dense(32, activation='selu'),
		# tf.keras.layers.Dense(8, activation='selu'),
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
	return chla,lon_list,lat_list


def train_pretreatment():
	return


def train():
	return


def save_model():
	return


if __name__ == '__main__':
	os.environ['PROJ_LIB'] = r'D:\Program Files\PostgreSQL\13\share\contrib\postgis-3.0\proj'
	excel_path = r'D:\Code\Al\9.22BYD\2021.9.22result.xlsx'
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
	DN = [444, 267, 390, 226, 309, 226, 357, 232, 377, 239, 433, 297,
	      437, 280, 432, 252, 515, 293, 554, 297, 475, 267, 409, 271, 405, 288,
	      343, 235, 435, 362, 400, 281, 399, 316, 363, 235, 409, 247, 401, 271]
	DN = np.array(DN)
	chla = [16, 20, 21, 16, 19, 9, 6, 7, 8, 8, 4, 5, 13, 7, 11, 10, 12, 15,
	        27, 15]
	# 数据预处理
	DN = lonlat2DN(dataset, lon_list, lat_list)
	chla = np.array(chla)
	# chla = standardization(chla)

	X_train = DN[:20]
	Y_train = chla[:10]
	print(X_train)

	m = np.mean(X_train)
	s = np.std(X_train)
	X_train = standardization(X_train)
	X_train = X_train.reshape(-1, 2)

	X_test = DN[28:]
	X_test = X_test.astype(np.float64)
	print(m)
	print(X_test)
	X_test -= m 
	X_test /= s
	X_test = X_test.reshape(-1, 2)
	Y_test = chla[14:]

	# 训练模型
	model = my_model()
	history = model.fit(X_train, Y_train,
	                    epochs=200,
	                    validation_split=0.25,
	                    batch_size=5
	                    )
	# 模型保存
	model.save(model_path)
	model.evaluate(X_test, Y_test)
	y = model.predict(X_test)


