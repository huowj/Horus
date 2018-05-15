#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 22:14:53 2018

@author: hwj
"""

#import csv
import scipy
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from OEMV import OEMV
from sklearn import metrics

data=pd.read_csv("/hwj/yahoo/python/data/A2Benchmark/synthetic_2.csv")
value=data.value
is_anomaly=data.is_anomaly

#with open("/hwj/yahoo/python/data/A1Benchmark/real_5.csv") as f:
#  reader = csv.DictReader(f)
#  value = [float(row['value']) for row in reader]

def DoubleWindowMV(value,m,n,epsilon, liwen):
    #initialize mean and var
    epsilon=0.9999999999
    T_length=len(value)
    T_dist=[0]*(T_length)
    predict=[0]*(T_length)
    mean_array=[]
    var_array=[]
    index=1
    for i in range(m,T_length-n+1):
        nearest_neighbor_dist=np.infty
        label=0
        for j in range(i-m,i-n+1):
            a=np.array(value[i:i+n])
            b=np.array(value[j:j+n])
            dist=np.linalg.norm(a-b)
            if dist<nearest_neighbor_dist:
                nearest_neighbor_dist=dist
        T_dist[i]=nearest_neighbor_dist
        
        if i-m>5:
            (mean,var) = liwen.getMeanSD()
            mean_array.append(mean)
            var_array.append(var)
            z_epsilon=scipy.stats.norm(0,var).ppf(epsilon)
            if nearest_neighbor_dist>(mean+z_epsilon):
                predict[i]=1
            else:
                liwen.update(nearest_neighbor_dist)
        else:
            liwen.update(nearest_neighbor_dist)
            
        """
        if i==m:
            var=0
        
        if label==0:
            var=var+(np.square(nearest_neighbor_dist-mean))*(index-1)/(index)
            mean=nearest_neighbor_dist/(index)+mean*(index-1)/(index)
            var_array.append(var)
            mean_array.append(mean)
            index=index+1
        """
    print(len(T_dist))
    x1=range(len(T_dist))
    x2=range(len(value))
    plt.figure(1)
    plt.plot(x1,T_dist)
    plt.figure(2)
    plt.plot(x2,value)
    for i in x2:
        if is_anomaly[i]==1:
            plt.plot(i,value[i],'ro-')
    x3=range(len(var_array))
    plt.figure(3)
    plt.plot(x3,var_array)
    x4=range(len(mean_array))
    plt.figure(4)
    plt.plot(x4,mean_array)
    num=0
    for i in range(0,T_length):
        if(predict[i]==1):
            print(i)
            num+=1
    print('num =',num)
    classify_report = metrics.classification_report(is_anomaly, predict)
    confusion_matrix = metrics.confusion_matrix(is_anomaly, predict)
    print(classify_report)
    print(confusion_matrix)

if __name__ == "__main__":
    liwen = OEMV(0.95)
    DoubleWindowMV(value,100,3,0.1, liwen)