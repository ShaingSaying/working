# 计算沪深300指数2017年3月份的涨跌额（%）的方差、标准差
# 计算沪深300指数2017年3月份的涨跌额（%）与格力电器（SZ:000651）2017年3月份的协方差
import numpy as np

datas1 = [0.16, -0.67, -0.21, 0.54, 0.22, -0.15, -0.63, 0.03, 0.88, -0.04, 0.20, 0.52, -1.03, 0.11, 0.49, -0.47,
0.35, 0.80, -0.33, -0.24, -0.13, -0.82, 0.56]

datas2 = [0.07, -0.55, -0.04, 3.11, 0.28, -0.50, 1.10, 1.97, -0.31, -0.55, 2.06, -0.24, -1.44, 1.56, 3.69, 0.53,
2.30, 1.09, -2.63, 0.29, 1.30, -1.54, 3.19]

variance = np.var(datas1)

standard_deviation1 = np.std(datas1, ddof=0)
standard_deviation2 = np.std(datas2, ddof=0)

cov2 = np.cov(datas1, datas2, ddof=0)[1][0]

ppcc = cov2/(standard_deviation1*standard_deviation2)

print(str(variance))
print(str(standard_deviation1))
print(str(cov2))
print(str(ppcc))
