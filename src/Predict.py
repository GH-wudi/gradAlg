import time

import numpy as np
import shapefile
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from osgeo import gdal
from tensorflow.python import keras

from IO import get_band, read_para, write_image
from Train import standardization


def data_pretreatment(band):
	"""数据预处理

	:param nparray band: 未处理的影像数据
	:return nparray: 处理之后的影像数据
	"""
	if (True in np.isnan(band)):
		for i in range(len(band)):
			bandi = band[i][~np.isnan(band[0])]
	else:
		for i in range(len(band)):
			bandi = band[i][band[i] != np.max(band[i])]
	arr_tuple = tuple([bandi for i in range(len(band))])
	DN = np.stack(arr_tuple, axis=1)
	DN = standardization(DN).reshape(-1, len(band))
	return DN


def predict(band):
	"""根据建好的模型进行预测

	:param nparray band: 原始影像
	:return nparray: 预测好的影像
	"""
	model = keras.models.load_model('./model')
	y = model.predict(data_pretreatment(band))
	y = np.abs(y.astype(np.uint8))
	return y


def format_img(band, y):
	"""格式化图片

	:param nparray band: 波段数组
	:param nparray y: 预测生成的影像
	:return nparray: 格式化之后的影像
	"""
	img = np.zeros(band[0].shape, np.uint8)
	if (True in np.isnan(band[0])):
		row, col = np.where(~np.isnan(band[0]))
	else:
		row, col = np.where(band[0] != np.max(band[0]))
	for i in range(len(y)):
		img[row[i], col[i]] = y[i]
	return img


def mask(image, shp_file, out_path):
	"""掩膜，根据shp文件进行裁剪

	:param gdal_image image: 传入的影像
	:param String shp_file: shp文件的路径
	:param String out_path: 裁剪完成的数据生成路径
	"""
	shp = shapefile.Reader(shp_file)
	ds = gdal.Warp(out_path,
	               image,
	               format='GTiff',
	               outputBounds=shp.bbox,
	               cutlineDSName=shp_file,
	               dstNodata=0)
	del ds


#  叶绿素反演
def visualization(img, out_path, cmap, dpi):
	"""用matplotlib绘制反演好的图片

	:param nparray img: 影像的数组
	:param String out_path: 影像保存路径
	:param String cmap: matplotlib的颜色配置参数
	:param int dpi: 像素密度
	"""
	img[img > 200] = 0
	norm = plt.Normalize(vmin=np.nanmin(img), vmax=np.nanmax(img))
	fig = plt.figure()
	im = plt.imshow(img, cmap=cmap, norm=norm)
	ChineseFont = FontProperties(fname=r'c:\windows\fonts\STXINGKA.TTF', size=14)
	plt.axis('off')
	plt.title('白洋淀叶绿素a浓度', font=ChineseFont)
	position = fig.add_axes([0.82, 0.12, 0.015, 0.30])  # 位置[左,下,右,上]
	cb = plt.colorbar(im, cax=position)

	# 设置colorbar标签字体等
	colorbar_font_dict = {"size": 7, "color": "k", 'family': 'Times New Roman'}
	cb.ax.set_title('Values(µg/L)', fontdict=colorbar_font_dict, pad=6)
	cb.ax.set_ylabel('ChlorophyllA(Chla)', fontdict=colorbar_font_dict)
	cb.ax.tick_params(labelsize=4, direction='in')
	plt.savefig(out_path,
	            bbox_inches='tight',
	            dpi=dpi
	            )


if __name__ == '__main__':
	start = time.perf_counter()
	para = read_para('./parameters.json')
	pred = para["predict"]
	# mask(pred["img"],pred["shp_file"],pred["out_tif"])
	dataset = gdal.Open(pred["img"])
	bands = get_band(dataset, pred["bands"])
	result = predict(bands)

	img_format = format_img(bands, result)
	write_image(dataset, pred["out_tif"], img_format, 1)
	visualization(img_format, pred["out_img"], pred["cmap"], pred["dpi"])

	end = time.perf_counter()
	print("time:%.3fs" % (end - start))
	print('end')
