# coding: utf-8
# The code is written by wfh
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
	with open(path, 'r', encoding='utf-8') as f:
		return json.load(f)


def write_json(path,data):
	with open(path,'w') as f:
		json.dump(data,f)


def make_dir(path):
	"""
	@param path:
	@return:
	"""
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)
		print('successful')
	else:
		return
