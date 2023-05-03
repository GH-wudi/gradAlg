import numpy as np

from IO import read_json, write_json


def standardization(data):
	"""数据标准化

	:param nparray data: 需要标准化的数据
	:return nparray: 标准化之后的数据
	"""
	# ? np.mean(data,axis = 0)计算出来的结果不一样
	mu = np.mean(data)
	sigma = np.std(data)
	return (data - mu) / sigma


def pearson(x, y):
	"""计算皮尔逊相关系数

	:param list x: 此处指像元值
	:param list y: 此处指叶绿素a浓度
	:return list: 相关系数列表
	"""
	pccs_list = []
	for i in range(len(x)):
		pccs = np.corrcoef(x[i], y)
		pccs_list.append(abs(pccs[1][0]))
	return pccs_list


def write_data(key: str, value: list):
	dic = {
		key: value
	}
	write_json('../data/result.json', dic)


if __name__ == "__main__":
	data = read_json('../data/data.json')
	chla = data['chla']
	dn = data['DN']
	# dn = np.array(dn)
	# dn = standardization(dn)
	# chla = standardization(chla)
	# pccses = pearson(dn, chla)
	print(dn[0:10])
	# write_data('pccs', pccses)
    
# * 数据是否标准化计算出来的Pearson相关系数是一样的


