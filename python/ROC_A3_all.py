#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 20:27:32 2018

@author: hwj
"""

#import csv
import math
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from sklearn import metrics

A3_p=pd.read_csv("/hwj/yahoo/distance/tricks/A3.csv")

#anomaly_table=np.zeros((1680,100))
#for p in range(100):
#    data=pd.read_csv("/hwj/yahoo/python/data/A3Benchmark/A3Benchmark-TS"+str(p+1)+".csv")
#    is_anomaly=data.anomaly
#    for m in range(len(is_anomaly)):
#        if is_anomaly[m]==1:
#            is_anomaly[m-1]=1
#            is_anomaly[m-2]=1
#    anomaly_table[:,p]=np.array(is_anomaly)
#np.savetxt("/hwj/yahoo/distance/A3/probability/A3_anomaly_transfer.csv", anomaly_table, delimiter = ',')


table=np.zeros((500,9))

for i in range(500):
    tp_all=0
    fn_all=0
    fp_all=0
    tn_all=0
    for index in range(100):
        data=pd.read_csv("/hwj/yahoo/python/data/A3Benchmark/A3Benchmark-TS"+str(index+1)+".csv")
        p_table=pd.read_csv("/hwj/yahoo/distance/A3/probability/A3_probability_"+str(index+1)+".csv",header=None)
        norm_a=A3_p.norm_a[index]
        is_anomaly=data.anomaly
        predict_probability=p_table.iloc[:,4]
        norm_window=A3_p.norm_window[index]
        norm_transition=A3_p.norm_transition[index]
        norm_sub=A3_p.norm_sub[index]
        is_anomaly_1=np.array(is_anomaly[norm_window+norm_transition:1681-norm_sub])
        threshold=norm_a+(i-300)*0.002
        length=len(predict_probability)
        predict=[0]*length
        for j in range(length):
            if predict_probability[j]>threshold:
                predict[j]=1
        for m in range(4,len(predict)-3):
            if (is_anomaly_1[m]==1):
                flag=0
                for j in range(-3,3):
                    if(predict[j+m]==1):
                        flag=1
                if (flag==1):
                    for q in range(-3,3):
                        predict[m+q]=is_anomaly_1[m+q]
        conf_mat = metrics.confusion_matrix(is_anomaly_1, predict)
        tp=conf_mat[1,1]
        fn=conf_mat[1,0]
        fp=conf_mat[0,1]
        tn=conf_mat[0,0]
        tp_all+=tp
        fn_all+=fn
        fp_all+=fp
        tn_all+=tn
    precision=tp_all/(tp_all+fp_all)
    recall=tp_all/(tp_all+fn_all)
    tpr=recall
    fpr=fp_all/(fp_all+tn_all)
    print(tp_all,fn_all,fp_all,tn_all,precision,recall,tpr,fpr)
    table[i,0]=tp_all
    table[i,1]=fn_all
    table[i,2]=fp_all
    table[i,3]=tn_all
    table[i,4]=precision
    table[i,5]=recall
    table[i,6]=tpr
    table[i,7]=fpr
    table[i,8]=(i-500)*0.0001
    print(i)
                
np.savetxt("/hwj/yahoo/distance/A3/probability/A3_all.csv", table, delimiter = ',')
plt.plot(table[:,7],table[:,6])
plt.plot(table[:,4],table[:,5])        
            
#for index in range(100):
#    data=pd.read_csv("/hwj/yahoo/python/data/A3Benchmark/A3Benchmark-TS"+str(index)+"1.csv")
#    p_table=pd.read_csv("/hwj/yahoo/distance/A3/probability/A3_probability_"+str(index)+"1.csv",header=None)
#    A3_p=pd.read_csv("/hwj/yahoo/distance/tricks/A3.csv")
#    norm_a=A3_p.norm_a[index]
#    is_anomaly=data.anomaly
#    predict_probability=p_table.iloc[:,4]
#    norm_window=A3_p.norm_window[index]
#    norm_transition=A3_p.norm_transition[index]
#    norm_sub=A3_p.norm_sub[index]
#    is_anomaly_1=np.array(is_anomaly[norm_window+norm_transition:1681-norm_sub])
#    print(norm_a)
#    print(predict_probability[0:4])
#    table=np.zeros((1000,9))
    