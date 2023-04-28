// package com.myself.raster;

import org.gdal.gdal.Band;
import org.gdal.gdal.Dataset;
import org.gdal.gdal.Driver;
import org.gdal.gdal.gdal;
import org.gdal.gdalconst.gdalconstConstants;

import java.util.Arrays;

public class RasterDemo {

    public static void main(String[] args) {
        String filepath = "F:\\raster\\Demo.tif";
        // 注册驱动
        gdal.AllRegister();
        // 打开文件获取数据集
        Dataset self = gdal.Open(filepath,
                gdalconstConstants.GA_ReadOnly);
        if (self == null) {
            System.out.println("打开" + filepath + "失败" + gdal.GetLastErrorMsg());
            System.exit(1);
        }
        // 获取驱动
        Driver driver = self.GetDriver();
        // 获取驱动信息
        System.out.println("driver long name: " + driver.getLongName());
        // 获取栅格数量
        int bandCount = self.getRasterCount();
        System.out.println("RasterCount: " + bandCount);
        // 构造仿射变换参数数组，并获取数据
        double[] gt = new double[6];
        self.GetGeoTransform(gt);
        System.out.println("仿射变换参数" + Arrays.toString(gt));

        // 指定经纬度
        double Latitude = 86.053;
        double longitude = 16.529;

        // 经纬度转换为栅格像素坐标
        int[] ColRow = Coordinates2ColRow(gt, Latitude, longitude);

        // 判断是否坐标超出范围
        if (ColRow[0] < 0 || ColRow[1] < 0 || ColRow[0] > self.getRasterXSize()
                || ColRow[1] > self.getRasterYSize()) {
            System.out.println(Arrays.toString(ColRow) + "坐标值超出栅格范围！");
            return;
        }

        // 遍历波段，获取该点对应的每个波段的值并打印到屏幕
        for (int i = 0; i < bandCount; i++) {
            Band band = self.GetRasterBand(1);
            double[] values = new double[1];
            band.ReadRaster(ColRow[0], ColRow[1], 1, 1, values);
            double value = values[0];
            System.out.println("横坐标：" + Latitude + "," + "纵坐标:" + longitude);
            System.out.format("Band" + (i + 1) + ": %s", value);
        }

    }

    /**
     * 将地图坐标转换为栅格像素坐标
     * 
     * @param gt 仿射变换参数
     * @param X  横坐标
     * @param Y  纵坐标
     * @return
     */
    public static int[] Coordinates2ColRow(double[] gt, double X, double Y) {
        int[] ints = new int[2];
        // X = gt[0] + Xpixel*gt[1] + Yline*gt[2];
        // Y = gt[3] + Xpixel*gt[4] + Yline*gt[5];
        // 消元法解二元一次方程组
        // X-gt[0]=Xpixel*gt[1] + Yline*gt[2]
        // Xpixel = (X-gt[0] - Yline*gt[2])/gt[1]
        // Y - gt[3] = ((X-gt[0] - Yline*gt[2])/gt[1])gt[4] + Yline*gt[5]
        // (Y - gt[3])*gt[1] = ((X-gt[0] - Yline*gt[2]))*gt[4] + Yline*gt[5]*gt[1]
        // (Y - gt[3])*gt[1] =(X-gt[0])*gt[4] - Yline*gt[2]*gt[4] + Yline*gt[5]*gt[1]
        // (Y - gt[3])*gt[1] - (X-gt[0])*gt[4] = Yline(gt[5]*gt[1]-gt[2]*gt[4])

        // 向下取整,如果向上取整会导致计算结果偏大，从而在后面读取到邻近像元的数据
        double Yline = Math.floor(((Y - gt[3]) * gt[1] - (X - gt[0]) * gt[4]) / (gt[5] * gt[1] - gt[2] * gt[4]));
        double Xpixel = Math.floor((X - gt[0] - Yline * gt[2]) / gt[1]);
        ints[0] = new Double(Xpixel).intValue();
        ints[1] = new Double(Yline).intValue();
        return ints;
    }

}