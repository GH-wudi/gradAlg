"""
Author: Emc2 emc-ironh@qq.com
Date: 2022-01-22 17:59:22
LastEditors: Emc2 emc-ironh@qq.com
LastEditTime: 2023-04-17 17:54:36
Description:

Copyright (c) 2023 by wfh, All Rights Reserved.
"""
import json
import os

import numpy as np
from osgeo import gdal


type_map={
	"int8"     :gdal.GDT_Byte,
    "uint8"    :gdal.GDT_Byte,
    "uint16"   :gdal.GDT_UInt16,
    "int16"    :gdal.GDT_Int16,
    "uint32"   :gdal.GDT_UInt32,
    "int32"    :gdal.GDT_Int32,
	"int64"    :gdal.GDT_Float32,
    "float32"  :gdal.GDT_Float32,
    "float64"  :gdal.GDT_Float64,
    "int16"    :gdal.GDT_CInt16,
    "complex64":gdal.GDT_CInt32,
    "complex64":gdal.GDT_CFloat32,
    "complex64":gdal.GDT_CFloat64
}


def get_band(ds, band_list=None):
	"""读取影像波段

	:param GDAL_dataset ds: gdal的数据集
	:param list band_list: 波段列表, defaults to None
	:return np_array: 将波段读取为数组的方式并返回
	"""
	if ds is None:
		print("数据集不能为空")
		return
	if band_list is None:
		band_list = list(range(1, ds.RasterCount + 1))
	band_arr = []
	for i in band_list:
		bandi = ds.GetRasterBand(i).ReadAsArray()
		band_arr.append(bandi)
	band_arr = np.array(band_arr)
	return band_arr


def write_image(dataset, out_path, a, bands):
	"""创建影像

	:param gdal_ds dataset: gdal的数据集
	:param String out_path: 输出路径
	:param nparray a: 写进影像的数组
	:param int bands: 波段数量
	"""
	if dataset is None:
		print("数据集不能为空")
		return
	# bands = a.shape
	tiff_driver = gdal.GetDriverByName('GTIFF')
	out = tiff_driver.Create(out_path,
	                         dataset.RasterXSize,
	                         dataset.RasterYSize,
	                         bands,
							 eType=type_map[a.dtype.name]
	                         )
	out.SetProjection(dataset.GetProjection())
	out.SetGeoTransform(dataset.GetGeoTransform())
	del dataset
	for band in range(bands):
		out.GetRasterBand(band + 1).WriteArray(a)
		out.FlushCache()
		out.BuildOverviews('average', [2, 4, 8, 16, 32])
	del out


def read_para(path):
	"""读取参数

	:param String path: 参数json文件所在的位置
	:return json/dict: 返回读取到的参数，格式为json或者字典
	"""
	with open(path, 'r', encoding='utf-8') as f:
		return json.load(f)


def write_json(path,data):
	"""写入到json文件里

	:param String path: 要保存的路径
	:param dict data: 要写入的数据
	"""
	with open(path,'w') as f:
		json.dump(data,f)


def make_dir(path):
	"""创建文件夹

	:param string path: 要创建文件夹的路径
	"""
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)
		print('successful')
	else:
		return
