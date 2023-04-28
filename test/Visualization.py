
from matplotlib import pyplot as plt
from IO import write_json
from osgeo import gdal

ds = gdal.Open('./img/test.tif')
img = ds.GetRasterBand(1).ReadAsArray()
img[img > 200] = 0
img_dict={
    'img':img.tolist()
}
write_json('./test/test.json',img_dict)

# data_min = np.nanmin(img)
# data_max = np.nanmax(img)
#
# vmin = data_min
# vmax = data_max
# # Normalize()跟归一化没有任何关系，函数的作用是将颜色映射到vmin-vmax上，
# # 颜色表/颜色柱的起始和终止分别取值vmin和vmax
# norm = plt.Normalize(vmin=vmin, vmax=vmax)
# fig = plt.figure()
# im1 = plt.imshow(img, norm=norm, cmap='Greens')
# ChineseFont = FontProperties(fname=r'c:\windows\fonts\STXINGKA.TTF', size=14)
# plt.axis('off')
# plt.title('白洋淀叶绿素a浓度', font=ChineseFont)
# # plt.text(.8, -.02, '\nVisualization by DataCharm', transform=im1.ax.transAxes, ha='center', \
# #          va='center', fontsize=10, color='black')
#
#
# position = fig.add_axes([0.82, 0.12, 0.015, 0.30])  # 位置[左,下,右,上]
# cb = plt.colorbar(im1, cax=position)
#
# # 设置colorbar标签字体等
# colorbarfontdict = {"size": 7, "color": "k", 'family': 'Times New Roman'}
# cb.ax.set_title('Values(µg/L)', fontdict=colorbarfontdict, pad=6)
# cb.ax.set_ylabel('ChlorophyllA(Chla)', fontdict=colorbarfontdict)
# cb.ax.tick_params(labelsize=4, direction='in')
# manager = plt.get_current_fig_manager()

# manager.window.showMaximized()
plt.savefig('./img/result_n.png',
            bbox_inches='tight',
            dpi=600,
            )

# plt.show()

# norm = colors.Normalize(vmin = data_min,vmax = data_max)

# im = plt.imshow(img,cmap='Greens',norm=norm)
# plt.colorbar()
# plt.savefig('./img/test2.png',dpi=1000)
# plt.show()
