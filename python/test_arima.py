#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 19:55:30 2017

@author: hwj
"""

import pandas as pd
import pyflux as pf
# -*- coding: utf-8 -*-import pandas as pdimport pyflux as pfimport matplotlib.pyplot as plt
print('starting...')# 数据读取
data = pd.read_csv('./value.csv')# 构建模型，默认差分次数为0
model = pf.ARIMA(data=data, ar=10, ma=10, integ=1, target='x', family=pf.Normal())
print('calculating parameters...')# 参数估计：点估计
model.fit("MLE")# 预测紧接下来60个数据
p_data = model.predict(h=60)

# 绘图部分
xx = range(2000)
plt.plot(xx, data['x'])
x_p = range(2000, 2060)
plt.plot(x_p, p_data)
print('showing...')
plt.show()