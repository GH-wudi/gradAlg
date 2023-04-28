import numpy as np
import pandas as pd
from toEach import lonlat2imagexy


def read_data(excel_path, sheet_name, usecols):
    """读取excel数据

    :param str excel_path: excel表格的路径
    :param str sheet_name: 表格名字
    :param list usecols: 列的数量
    :return nparray: 以nparray的数据格式返回
    """
    sheet = pd.read_excel(
        io=excel_path, sheet_name=sheet_name, usecols=usecols)
    return np.array(sheet.values)


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
        radiation_value = dataset.ReadAsArray(row, col, 1, 1)
        for j in range(32):
            DN.append(radiation_value[j][0][0])
    # np.concatenate((DN[0][0],DN[1][0]),axis=0)
    # for j in range(32):
    # 	DN.insert(j+1,DNi[j])
    # DN.append(radiation_value[13][0][0])
    # DN = standardization(DN)
    DN = np.array(DN)
    return DN


def write_data(xlsPath: str):
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    df.to_excel(xlsPath)


def writeDataIntoExcel(xlsPath: str, data: dict):
	writer = pd.ExcelWriter(xlsPath)
	sheetNames = data.keys()  # 获取所有sheet的名称
	# sheets是要写入的excel工作簿名称列表
	data = pd.DataFrame(data)
	for sheetName in sheetNames:
		data.to_excel(writer, sheet_name=sheetName)
	# 保存writer中的数据至excel
	# 如果省略该语句，则数据不会写入到上边创建的excel文件中
	writer.save()


if __name__ == '__main__':
    write_data('test.xlsx')
    # lonlat2DN()
    data = read_data(r'../9.22BYD/2021.9.22result.xlsx', 'Chla', [4, 5, 6])
    chla, lon_list, lat_list = data[:, 0], data[:, 1], data[:, 2]
    print(chla)
    print(lon_list)
    print(lat_list)
