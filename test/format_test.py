import numpy as np

from osgeo import gdal

img_path = 'D:\\Code\\Al\\jz\\rpcortho_bydquyu_jz.tif'
ds = gdal.Open(img_path)
img = ds.GetRasterBand(1).ReadAsArray()
print(np.min(img))


# row,col=np.where(~np.isnan(img))
row,col=np.where(img!=np.max(img))
# print(num_index[0].shape)

print(img[row[0],col[0]])