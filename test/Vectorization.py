# _*_ coding: utf-8 _*_

import sys
import os
import io
import cv2
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 打印出中文字符
try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import gdal
    import ogr
    import osr


def raster2shp(src="extracted_img.tif"):
    """
    函数输入的是一个二值影像，利用这个二值影像，创建shp文件
    """
    # src = "extracted_img.tif"
    # 输出的shapefile文件名称
    tgt = "extract.shp"
    # 图层名称
    tgtLayer = "extract"
    # 打开输入的栅格文件
    srcDS = gdal.Open(src)
    # 获取第一个波段
    band = srcDS.GetRasterBand(1)
    # 让gdal库使用该波段作为遮罩层
    mask = band
    # 创建输出的shapefile文件
    driver = ogr.GetDriverByName("ESRI Shapefile")
    shp = driver.CreateDataSource(tgt)
    # 拷贝空间索引
    srs = osr.SpatialReference()
    srs.ImportFromWkt(srcDS.GetProjectionRef())
    layer = shp.CreateLayer(tgtLayer, srs=srs)
    # 创建dbf文件
    fd = ogr.FieldDefn("DN", ogr.OFTInteger)
    layer.CreateField(fd)
    dst_field = 0
    # 从图片中自动提取特征
    extract = gdal.Polygonize(band, mask, layer, dst_field, [], None)


def calc_area():
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(
        "D:\\CodePython\\rasters2vector\\test\\test5.shp", 1)
    layer = dataSource.GetLayer()
    new_field = ogr.FieldDefn("Area", ogr.OFTReal)
    new_field.SetWidth(32)
    new_field.SetPrecision(2)  # 设置面积精度
    layer.CreateField(new_field)
    for feature in layer:
        geom = feature.GetGeometryRef()
        area = geom.GetArea()  # 计算面积
        # m_area = (area/(0.0089**2))*1e+6  # 单位由十进制度转为米
        # print(m_area)
        feature.SetField("Area", area)  # 将面积添加到属性表中
        layer.SetFeature(feature)
    dataSource = None


def WriteVectorFile():
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING", "")

    strVectorFile = "E:\\TestPolygon.shp"

    # 注册所有的驱动
    ogr.RegisterAll()

    # 创建数据，这里以创建ESRI的shp文件为例
    strDriverName = "ESRIShapefile"
    oDriver = ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("%s 驱动不可用！\n", strDriverName)
        return

    # 创建数据源
    oDS = oDriver.CreateDataSource(strVectorFile)
    if oDS == None:
        print("创建文件【%s】失败！", strVectorFile)
        return

    # 创建图层，创建一个多边形图层，这里没有指定空间参考，如果需要的话，需要在这里进行指定
    papszLCO = []
    oLayer = oDS.CreateLayer("TestPolygon", None, ogr.wkbPolygon, papszLCO)
    if oLayer == None:
        print("图层创建失败！\n")
        return

    # 下面创建属性表
    # 先创建一个叫FieldID的整型属性
    oFieldID = ogr.FieldDefn("FieldID", ogr.OFTInteger)
    oLayer.CreateField(oFieldID, 1)

    # 再创建一个叫FeatureName的字符型属性，字符长度为50
    oFieldName = ogr.FieldDefn("FieldName", ogr.OFTString)
    oFieldName.SetWidth(100)
    oLayer.CreateField(oFieldName, 1)

    oDefn = oLayer.GetLayerDefn()

    # 创建三角形要素
    oFeatureTriangle = ogr.Feature(oDefn)
    oFeatureTriangle.SetField(0, 0)
    oFeatureTriangle.SetField(1, "三角形")
    geomTriangle = ogr.CreateGeometryFromWkt("POLYGON ((0 0,20 0,10 15,0 0))")
    oFeatureTriangle.SetGeometry(geomTriangle)
    oLayer.CreateFeature(oFeatureTriangle)

    # 创建矩形要素
    oFeatureRectangle = ogr.Feature(oDefn)
    oFeatureRectangle.SetField(0, 1)
    oFeatureRectangle.SetField(1, "矩形")
    geomRectangle = ogr.CreateGeometryFromWkt(
        "POLYGON ((30 0,60 0,60 30,30 30,30 0))")
    oFeatureRectangle.SetGeometry(geomRectangle)
    oLayer.CreateFeature(oFeatureRectangle)

    # 创建五角形要素
    oFeaturePentagon = ogr.Feature(oDefn)
    oFeaturePentagon.SetField(0, 2)
    oFeaturePentagon.SetField(1, "五角形")
    geomPentagon = ogr.CreateGeometryFromWkt(
        "POLYGON ((70 0,85 0,90 15,80 30,65 15,700))")
    oFeaturePentagon.SetGeometry(geomPentagon)
    oLayer.CreateFeature(oFeaturePentagon)

    oDS.Destroy()
    print("数据集创建完成！\n")

img_path = 'D:\\CodePython\\rasters2vector\\test4.png'
img0 = cv2.imread(img_path)
# 转灰度
img1 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
ret, img2 = cv2.threshold(img1, 200, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(
    img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 提取二值图的所有轮廓边界
# print(contours)
# img = cv2.drawContours(img0, contours, -1, (0, 255, 0), 3)
# cv2.imshow("rotation", img)
# cv2.waitKey()
# cv2.destroyAllWindows()

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")  # 为了支持中文路径
gdal.SetConfigOption("SHAPE_ENCODING", "CP936")  # 为了使属性表字段支持中文
strVectorFile = "D:\\CodePython\\rasters2vector\\test\\test4.shp"  # 定义写入路径及文件名
ogr.RegisterAll()  # 注册所有的驱动
strDriverName = "ESRI Shapefile"  # 创建数据，这里创建ESRI的shp文件
oDriver = ogr.GetDriverByName(strDriverName)
if oDriver == None:
    print("%s 驱动不可用！\n", strDriverName)

oDS = oDriver.CreateDataSource(strVectorFile)  # 创建数据源
if oDS == None:
    print("创建文件【%s】失败！", strVectorFile)

srs = osr.SpatialReference()  # 创建空间参考
srs.ImportFromEPSG(4326)  # 定义地理坐标系WGS1984
papszLCO = []
# 创建图层，创建一个多边形图层,"TestPolygon"->属性表名
oLayer = oDS.CreateLayer("TestPolygon", srs, ogr.wkbPolygon, papszLCO)
if oLayer == None:
    print("图层创建失败！\n")

'''下面添加矢量数据，属性表数据、矢量数据坐标'''
oFieldID = ogr.FieldDefn("FieldID", ogr.OFTInteger)  # 创建一个叫FieldID的整型属性
oLayer.CreateField(oFieldID, 1)

oDefn = oLayer.GetLayerDefn()  # 定义要素
gardens = ogr.Geometry(ogr.wkbMultiPolygon)  # 定义总的多边形集
i = 0
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 100:  # 面积大于n才保存
        # print(area)
        box1 = ogr.Geometry(ogr.wkbLinearRing)
        i += 1
        for point in contour:
            x_col = float(point[0, 1])
            y_row = float(point[0, 0])
            box1.AddPoint(y_row, x_col)
        oFeatureTriangle = ogr.Feature(oDefn)
        oFeatureTriangle.SetField(0, i)
        garden1 = ogr.Geometry(ogr.wkbPolygon)  # 每次重新定义单多变形
        garden1.AddGeometry(box1)  # 将轮廓坐标放在单多边形中
        gardens.AddGeometry(garden1)  # 依次将单多边形放入总的多边形集中
gardens.CloseRings()  # 封闭多边形集中的每个单多边形，后面格式需要

geomTriangle = ogr.CreateGeometryFromWkt(str(gardens))  # 将封闭后的多边形集添加到属性表
oFeatureTriangle.SetGeometry(geomTriangle)
oLayer.CreateFeature(oFeatureTriangle)
oDS.Destroy()
print("数据矢量创建完成！\n")
