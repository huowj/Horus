#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 14:56:14 2018

@author: hwj
"""

#import csv
import math
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from sklearn import metrics


data=pd.read_csv("/hwj/yahoo/python/data/A3Benchmark/A3Benchmark-TS1.csv")
p_table=pd.read_csv("/hwj/yahoo/distance/A3/probability/A3_probability_1.csv",header=None)
A3_p=pd.read_csv("/hwj/yahoo/distance/tricks/A3.csv")
norm_a=A3_p.norm_a[0]
is_anomaly=data.anomaly
predict_probability=p_table.iloc[:,4]
norm_window=A3_p.norm_window[0]
norm_transition=A3_p.norm_transition[0]
norm_sub=A3_p.norm_sub[0]
is_anomaly_1=np.array(is_anomaly[norm_window+norm_transition:1681-norm_sub])

print(norm_a)
print(predict_probability[0:4])

table=np.zeros((1000,9))

#i=0
#threshold=norm_a-1
#length=len(predict_probability)
#predict=[0]*length
#for j in range(length):
#    if predict_probability[j]>threshold:
#        predict[j]=1
#is_anomaly=np.array(is_anomaly[norm_window+norm_transition:1681-norm_sub])
#print(len(is_anomaly))
#print(len(predict))
#print(is_anomaly[4])
#for m in range(4,len(predict)-3):
#    if (is_anomaly[m]==1):
#        flag=0
#        for p in range(-3,3):
#            if(predict[p+m]==1):
#                flag=1
#        if (flag==1):
#            for q in range(-3,3):
#                predict[m+q]=is_anomaly[m+q]
#conf_mat = metrics.confusion_matrix(is_anomaly, predict)
#tp=conf_mat[1,1]
#fn=conf_mat[1,0]
#fp=conf_mat[0,1]
#tn=conf_mat[0,0]
#precision=tp/(tp+fp)
#recall=tp/(tp+fn)
#tpr=recall
#fpr=fp/(fp+tn)
#f1=scipy.stats.hmean([precision,recall])
#f1=0
#print(conf_mat)
#table[i,0]=tp
#table[i,1]=fn
#table[i,2]=fp
#table[i,3]=tn
#table[i,4]=precision
#table[i,5]=recall
#table[i,6]=tpr
#table[i,7]=fpr
#table[i,8]=f1
#print(table)


for i in range(1000):
    threshold=norm_a+(i-500)*0.0001
    length=len(predict_probability)
    predict=[0]*length
    for j in range(length):
        if predict_probability[j]>threshold:
            predict[j]=1
    for m in range(4,len(predict)-3):
        if (is_anomaly_1[m]==1):
            flag=0
            for p in range(-3,3):
                if(predict[p+m]==1):
                    flag=1
            if (flag==1):
                for q in range(-3,3):
                    predict[m+q]=is_anomaly_1[m+q]
    conf_mat = metrics.confusion_matrix(is_anomaly_1, predict)
    tp=conf_mat[1,1]
    fn=conf_mat[1,0]
    fp=conf_mat[0,1]
    tn=conf_mat[0,0]
    precision=tp/(tp+fp)
    recall=tp/(tp+fn)
    tpr=recall
    fpr=fp/(fp+tn)
    table[i,0]=tp
    table[i,1]=fn
    table[i,2]=fp
    table[i,3]=tn
    table[i,4]=precision
    table[i,5]=recall
    table[i,6]=tpr
    table[i,7]=fpr
    table[i,8]=threshold

np.savetxt("/hwj/yahoo/distance/A3/probability/A3_1.csv", table, delimiter = ',')
plt.plot(table[:,7],table[:,6])
plt.plot(table[:,4],table[:,5])
            
