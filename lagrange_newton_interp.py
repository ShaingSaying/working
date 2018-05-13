# 拉格朗日法进行插补
import pandas as pd
from scipy.interpolate import lagrange    # 导入拉格朗日插值函数
inputfile ='../data/catering_sale.xls'
outputfile ='../tmptest/catering_sale1.xls'
data = pd.read_excel(inputfile)

# data[u'销量'][(data[u'销量'] < 400) | (data[u'销量'] > 5000)] = None #过滤异常值，将其变为空值
# data.loc[:,(u'销量',)][(data[u'销量'] < 400) | (data[u'销量'] > 5000)] = None #这是对处理后得到一个结果，不能作用到原数据上
row_indexs = (data[u'销量'] < 400) | (data[u'销量'] > 5000)
data.loc[row_indexs, u'销量'] = None
# 自定义列向量插值函数
# s为列向量，n为被插值的位置，k为取前后的数据个数，默认为5


def ployinterp_column(s, n, k=5):
    y = s[list(range(n-k, n)) + list(range(n+1, n+1+k))]  # 取数
    y = y[y.notnull()]  # 剔除空值
    return lagrange(y.index, list(y))(n)  # 插值并返回插值结果
# 逐个元素判断是否需要插值
for i in data.columns:
    for j in range(len(data)):
        if (data[i].isnull())[j]:  # 如果为空即插值。
            # data[i][j] = ployinterp_column(data[i], j)
            data.loc[j, i] = ployinterp_column(data[i], j)
# data.to_excel(outputfile) #输出结果，写入文件