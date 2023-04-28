import cv2 as cv
import numpy as np

from osgeo import gdal
from vector import polygonize,get_area
from indexes import *
from IO import *


# def tif2RGB(scrDS,destName):
#     options = gdal.TranslateOptions(format='PNG', bandList=[2, 7, 14])
#     gdal.Translate(destName, scrDS, options=options)


def chanel_one2three(img):
    img[img == 255] = 128
    BG = np.zeros(img.shape,np.uint8)
    return cv.merge([BG,BG,img])


def binaryzation(img,threshold):
    img[img >= threshold] = 255
    img[img <  threshold] = 0
    return img.astype(np.uint8)
 

def de_noising(img):
    """
    降噪，先腐蚀后膨胀，运用开运算
    """
    contours,hicrarchy = cv.findContours(img.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    temp = np.zeros(img.shape,np.uint8)
    contours.sort(key=lambda c: cv.contourArea(c), reverse=True)
    for i in range(5):
        temp += cv.drawContours(temp,[contours[i]],0,255,cv.FILLED)
    return temp



if __name__ == '__main__':
    image_path = r'D:\Code\Al\gf2_test.tif'
    out_path = r'C:\Users\Emc2\Desktop\test_RGB.png'
    out_path_tif = r'C:\Users\Emc2\Desktop\test.tif'
    shp_path = r'C:\Users\Emc2\Desktop\test2.shp'
    ESPG = 32650
    ds = gdal.Open(image_path)
    bands = get_band(ds,band_list=[2,4])
    NDWI = NDWI(bands[0],bands[1])  

    water_gray = de_noising(binaryzation(NDWI,-0.15))
    write_image(ds, out_path_tif, water_gray, 1)
    water_RGB = chanel_one2three(water_gray)
    cv.imwrite(out_path,water_RGB)
    # np.concatenate((DN[0][0],DN[1][0]),axis=0)
    # for j in range(32):
    # 	DN.insert(j+1,DNi[j])

    ds_gray = gdal.open(out_path_tif)
    polygonize(shp_path,ds_gray)
    get_area(shp_path,ESPG)
    print('end')

