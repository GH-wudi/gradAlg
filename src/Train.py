# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 11:45:03 2021
@author: wfh
"""
import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf

from osgeo import gdal
from IO import read_json
from toEach import lonlat2imagexy


def normalization(a):
    """数据正则化

    :param nparray a: 需要进行正则化的数据
    :return nparray: 正则化后的数据
    """
    return (a - np.min(a)) / (np.max(a) - np.min(a))


def standardization(data):
    """数据标准化

    :param nparray data: 需要标准化的数据
    :return nparray: 标准化之后的数据
    """
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma


def lonlat2DN(dataset, lon_list, lat_list):
    """读取对应经纬度点的像元值

    :param gdal_ds dataset: 影像数据
    :param list lon_list: 经度
    :param list lat_list: 纬度
    :return nparray: 对应的像元值
    """
    DN = []
    for i in range(len(lat_list)):
        row, col = lonlat2imagexy(dataset, lon_list[i], lat_list[i])
        radiation_value = dataset.ReadAsArray(row, col, 3, 3)
        for j in range(dataset.RasterCount):
            DN.append(radiation_value[j][0][0])
    # DN = standardization(DN)
    return np.array(DN)


def my_model():
    """tensorflow进行神经网络建模，模型有四层，输入层输出层对应数据，隐含层两层

    :return model: tf的model对象
    """
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


def read_data(excel_path, sheet_name, usecols):
    """读取excel数据

    :param str excel_path: excel表格的路径
    :param str sheet_name: 表格名字
    :param list usecols: 列的数量
    :return nparray: 以nparray的数据格式返回
    """
    sheet = pd.read_excel(
        io=excel_path, sheet_name=sheet_name, usecols=usecols)
    return sheet.values


if __name__ == '__main__':
    os.environ['PROJ_LIB'] = r'D:\Program Files\PostgreSQL\13\share\contrib\postgis-3.0\proj'

    excel_path = r'../9.22BYD/2021.9.22result.xlsx'
    image_path = r'D:/Code/Al/jz/rpcortho_bydquyu_jz.tif'
    sheet_name = 'Chla'
    model_path = './model'
    cols = [4, 5, 6]

    data = read_data(excel_path, sheet_name, cols)
    chla, lon_list, lat_list = data[:, 0], data[:, 1], data[:, 2]

    dataset = gdal.Open(image_path)
    DN = lonlat2DN(dataset, lon_list, lat_list)
    DN = DN.reshape(20, 32).T.tolist()
    print(DN)
    print(chla)
    # data_dict = {
    #     'DN': DN,
    #     'chal':chla.tolist()
    # }

    # with open('../data/data.json', 'w') as f:
    #     json.dump(data_dict,f)
    # pccs = np.corrcoef(chla,DN[0])
    # print(DN)
    # D = []
    # for i in range(len(DN)):
    # 	D.insert(i,DN[i][0])
    # print(D)
# DN = np.array(DN)
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
