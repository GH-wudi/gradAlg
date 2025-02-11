import numpy as np
from osgeo import osr

lonMeter = 0.00001141
latMeter = 0.00000899

# MeterParam = 0.00001 * 42496 / (124.44282531738276-124.3288421630859)
MeterParam = 3.7282702222226876


def getSRSPair(dataset):
	"""
	获得给定数据的投影参考系和地理参考系
	:param dataset: GDAL地理数据
	:return: 投影参考系和地理参考系
	"""
	prosrs = osr.SpatialReference()
	prosrs.ImportFromWkt(dataset.GetProjection())
	geosrs = prosrs.CloneGeogCS()
	return prosrs, geosrs


def geo2lonlat(dataset, x, y):
	"""
	将投影坐标转为经纬度坐标（具体的投影坐标系由给定数据确定）
	:param dataset: GDAL地理数据
	:param x: 投影坐标x
	:param y: 投影坐标y
	:return: 投影坐标(x, y)对应的经纬度坐标(lon, lat)
	"""
	prosrs, geosrs = getSRSPair(dataset)
	ct = osr.CoordinateTransformation(prosrs, geosrs)
	coords = ct.TransformPoint(x, y)
	return coords[:2]


def lonlat2geo(dataset, lon, lat):
	"""
	将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
	:param dataset: GDAL地理数据
	:param lon: 地理坐标lon经度
	:param lat: 地理坐标lat纬度
	:return: 经纬度坐标(lon, lat)对应的投影坐标
	"""
	prosrs, geosrs = getSRSPair(dataset)
	ct = osr.CoordinateTransformation(geosrs, prosrs)
	coords = ct.TransformPoint(lon, lat)
	return coords[:2]


def imagexy2geo(dataset, row, col):
	"""
	根据GDAL的六参数模型将影像图上坐标（行列号）转为投影坐标或地理坐标（根据具体数据的坐标系统转换）
	:param dataset: GDAL地理数据
	:param row: 像素的行号
	:param col: 像素的列号
	:return: 行列号(row, col)对应的投影坐标或地理坐标(x, y)
	"""
	trans = dataset.GetGeoTransform()
	px = trans[0] + col * trans[1] + row * trans[2]
	py = trans[3] + col * trans[4] + row * trans[5]
	return px, py


def geo2imagexy(dataset, x, y):
	"""
	根据GDAL的六 参数模型将给定的投影或地理坐标转为影像图上坐标（行列号）
	:param dataset: GDAL地理数据
	:param x: 投影或地理坐标x
	:param y: 投影或地理坐标y
	:return: 影坐标或地理坐标(x, y)对应的影像图上行列号(row, col)
	"""
	trans = dataset.GetGeoTransform()
	a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
	b = np.array([x - trans[0], y - trans[3]])
	return np.linalg.solve(a, b)  # 使用numpy的linalg.solve进行二元一次方程的求解


def imagexy2lonlat(dataset, row, col):
	"""
	影像行列转经纬度：
	：通过影像行列转平面坐标
	：平面坐标转经纬度
	"""
	coords = imagexy2geo(dataset, row, col)
	coords2 = geo2lonlat(dataset, coords[0], coords[1])
	return (coords2[0], coords2[1])


def lonlat2imagexy(dataset, lon, lat):
	"""
	影像经纬度转行列：
	：通过经纬度转平面坐标
	：平面坐标转影像行列
	"""
	coords = lonlat2geo(dataset, lon, lat)

	coords2 = geo2imagexy(dataset, coords[0], coords[1])
	return (int(round(abs(coords2[0]))), int(round(abs(coords2[1]))))



