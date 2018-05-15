#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:47:16 2018

@author: hwj
"""

import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv("/hwj/yahoo/python/data/A2Benchmark/synthetic_2.csv")
value=data.value
is_anomaly=data.is_anomaly

#with open("/hwj/yahoo/python/data/A1Benchmark/real_5.csv") as f:
#  reader = csv.DictReader(f)
#  value = [float(row['value']) for row in reader]

def DoubleWindowMV(value,m,n,epsilon):
    #initialize mean and var
    epsilon=0.35
    mean=0
    var=0
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
        z_epsilon=scipy.stats.norm(mean,(var**0.5)).ppf(1-epsilon)
        if i-m>5:
            if nearest_neighbor_dist>(mean+z_epsilon):
                predict[i]=1
                label=1
        if i==m:
            var=0
        if label==0:
            var=var+(np.square(nearest_neighbor_dist-mean))*(index-1)/(index)
            mean=nearest_neighbor_dist/(index)+mean*(index-1)/(index)
            var_array.append(var)
            mean_array.append(mean)
            index=index+1
            
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
    for i in range(0,T_length):
        if(predict[i]==1):
            print(i)

if __name__ == "__main__":
    DoubleWindowMV(value,150,3,0.1)