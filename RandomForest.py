# 使用随机森林算法做特征选择，在sklearn中调用已经封装好的算法
# UCI上葡萄酒的例子
import pandas as pd
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data'
df = pd.read_csv(url, header=None)
df.columns = ['Class label', 'Alcohol', 'Malic acid',
              'Ash', 'Alcalinity of ash', 'Magnesium', 'Total phenols',
              'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyains',
              'Color intensity', 'Hue', '0D280/0D315 of diluted wines', 'Proline']

import numpy as np
# 输出[1,2,3],一共为3个类别
print(np.unique(df['Class label']))

# 可见除去class label之外共有13个特征，数据集的大小为178.
print(df.info())

# 按照常规做法，将数据集分为训练集和测试集
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
x, y = df.iloc[:, 1:].values, df.iloc[:, 0].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
feat_labels = df.columns[1:]
forest = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=1)
forest.fit(x_train, y_train)

# 这样一来随机森林就训练好了，其中已经把特征的重要评估也做好了。
importances = forest.feature_importances_
indices = np.argsort(importances)[::-1]
for f in range(x_train.shape[1]):
    print("%2d) %-*s %f" % (f + 1, 30, feat_labels[f], importances[indices[f]]))

x_selected = forest.transform(x_train, threshold=0.15)
print(x_selected.shape)