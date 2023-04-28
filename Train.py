# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 11:45:03 2021
@author: wfh
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt


# from IO import *
# from toEach import lonlat2imagexy


def normalization(a):
    return (a - np.min(a)) / (np.max(a) - np.min(a))


def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma


# def lonlat2DN(dataset, lon_list, lat_list):
# 	DN = []
# 	for i in range(len(lat_list)):
# 		row, col = lonlat2imagexy(dataset, lon_list[i], lat_list[i])
# 		radiation_value = dataset.ReadAsArray(row, col, 1, 1)
# 		DN.append(radiation_value[2][0][0])
# DN.append(radiation_value[13][0][0])
# DN = np.array(DN).astype(np.uint32)
# DN = standardization(DN)
# return DN


#  模型


def my_model():
    model = tf.keras.models.Sequential([

        tf.keras.layers.Dense(12, activation='relu'),
        tf.keras.layers.Dense(12, activation='relu'),
        tf.keras.layers.Dense(12, activation='relu'),
        tf.keras.layers.Dense(12, activation='relu'),
        tf.keras.layers.Dense(12, activation='relu'),
        tf.keras.layers.Dense(12, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1)
    ])
    optimizers = [tf.keras.optimizers.Adam(learning_rate=0.5)]
    model.compile(optimizer='adam',
                  loss='mse',
                  metrics=['accuracy'])
    return model


# def read_data():
# 	sheet = pd.read_excel(io=excel_path, sheet_name=sheet_name, usecols=cols)
# 	data = np.array(sheet.values)
# 	chla, lon_list, lat_list = data[:, 0], data[:, 1], data[:, 2]
# 	return chla, lon_list, lat_list


if __name__ == '__main__':
    # os.environ['PROJ_LIB'] = r'D:\Program Files\PostgreSQL\13\share\contrib\postgis-3.0\proj'
    excel_path = r'D:\毕业设计\训练数据.xlsx'
    # image_path = r'D:\Code\Al\jz\rpcortho_bydquyu_jz.tif'
    sheet_name = 'Sheet1'
    model_path = './model'
    cols = [1, 2, 3, 4, 5, 6]
    col = ['森林碳储量(万t)']

    # 读取数据
    sheet = pd.read_excel(io=excel_path, sheet_name=sheet_name, usecols=cols)
    C = pd.read_excel(io=excel_path, sheet_name=sheet_name, usecols=col)
    A = np.array(sheet.values)
    C = np.array(sheet.values)
    # print(A)
    # a, b, c, d, e, f = data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4], data[:, 5]

    # dataset = gdal.Open(image_path)
    # raster_count = dataset.RasterCount

    # 数据预处理
    # DN = lonlat2DN(dataset, lon_list, lat_list)
    # A = np.hstack((a, b, c, d, e, f))
    A = np.array(A)
    C = np.array(C)
    A = standardization(A)
    C = standardization(C)
    # X = DN.reshape(-1, 1)
    X_train, X_test, Y_train, Y_test = train_test_split(A, C, test_size=0.3, random_state=2)

    m = np.mean(X_train)
    s = np.std(X_train)

    X_test -= m
    X_test /= s
    # X_test = X_test.reshape(-1, 2)
    # 训练模型
    model = my_model()
    history = model.fit(X_train, Y_train,
                        epochs=500,
                        validation_split=0.25,
                        batch_size=5
                        )
    # 模型保存
    model.save(model_path)
    model.evaluate(X_test, Y_test)
    y = model.predict(X_test)

    # 画图
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    # val_loss = history.history['val_loss']
    epochs = range(len(acc))

    plt.plot(epochs, acc, 'b', label='Training accuracy')
    plt.plot(epochs, val_acc, 'r', label='validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend(loc='lower right')
    plt.figure()

    plt.plot(epochs, loss, 'r', label='Training loss')
    # plt.plot(epochs, val_loss, 'b', label='validation loss')
    plt.title('Training  loss')
    plt.legend()
    plt.show()
