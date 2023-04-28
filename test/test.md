### 交叉验证

```python
from sklearn.model_selection import KFold

cvscores = []
kfold = KFold(n_splits=10, shuffle=True,random_state=10)
for train, test in kfold.split(X_train,Y_train):
	history = model.fit(X_train[train],X_train[train],
	                    epochs=100,
	                    #validation_split=.25,
	                    )
	scores = model.evaluate(X_train[test, Y_train[test], verbose=0)
	print("%s: %.2f%%" % (modelmetrics_names[1], scores[1] * 100))
	cvscores.append(scores[1] * 100)
print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
```
### 坐标互转
```python
if __name__ == '__main__':
	os.environ['PROJ_LIB'] = r'D:\Program Files\PostgreSQL\13\share\contrib\postgis-3.0\proj'
	ds = gdal.Open(r'D:\Code\Al\HGM1result\HGM1.tif')
	raster_count = ds.RasterCount
	print(raster_count)
	lon = 115.98832093
	lat = 38.90084696
	lon, lat = gcj02_to_wgs84(lon, lat)
	print(lon, lat)
	row, col = lonlat2imagexy(ds, lon, lat)
	print(row, col)
	band = ds.GetRasterBand(7)
	# radiation_value = ds.ReadRaster(row,col,1,1,band_list = [7,14])
	radiation_value = ds.ReadRaster(row, col, 1, 1)
	# declaring byte value
	print(radiation_value[7, 14])
intval = struct.unpack('h', radiation_value)  # use the 'double' format code 4 bytes
print(intval)
converting to int
byteorder is big where MSB is at start
int_val = int.from_bytes(radiation_value, "little")

printing int equivalent
print(int_val)
```

