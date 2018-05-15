#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:57:28 2018

@author: hwj
"""

#import csv
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from sklearn import metrics

data=pd.read_csv("/hwj/yahoo/python/data/A1Benchmark/real_65.csv")
value=data.value
is_anomaly=data.is_anomaly

#with open("/hwj/yahoo/python/data/A1Benchmark/real_5.csv") as f:
#  reader = csv.DictReader(f)
#  value = [float(row['value']) for row in reader]

def DoubleWindowMV(value,m,n,epsilon,lamda):
    #initialize mean and var
    epsilon=0.0001
    mean=0
    var=10000000000000000
    T_length=len(value)
    T_dist=[0]*(T_length)
    predict=[0]*(T_length)
    mean_array=[0]
    var_array=[0]
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
            #######################with lamda forget factor###########################
            var=var*lamda*(1-lamda**(index-1))/(1-lamda**index)+(np.square(nearest_neighbor_dist-mean))*lamda*(1-lamda)*(1-lamda**(index-1))/np.square(1-lamda**(index))
            mean=nearest_neighbor_dist*(1-lamda)/(1-lamda**(index))+mean*lamda*(1-lamda**(index-1))/(1-lamda**(index))
            var_array.append(var)
            mean_array.append(mean)
            index=index+1
    print(len(T_dist))
    x1=range(0,len(T_dist))
    x2=range(0,len(value))
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
    predict_num=0
    for i in range(0,T_length):
        if(predict[i]==1):
            print(i)
            predict_num+=1
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    ####################f1 adjustment###########################
    for i in range(0,T_length):
        if(is_anomaly[i]==1):
            print(i)
    predict_adjust=[0]*(T_length)
    for i in range(0,T_length-1):
        if((predict[i]==1) & (predict[i+1]==1) & ((i+n-1)<T_length-1)):
            predict_adjust[i+n-1]=1
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    for i in range(0,T_length):
        if(predict_adjust[i]==1):
            print(i)
#    for i in range(0,T_length)
        
    print(predict_num)
    classify_report = metrics.classification_report(is_anomaly, predict)
    confusion_matrix = metrics.confusion_matrix(is_anomaly, predict)
    classify_report1 = metrics.classification_report(is_anomaly,predict_adjust)
    confusion_matrix1 = metrics.confusion_matrix(is_anomaly,predict_adjust)
    print(classify_report)
    print(confusion_matrix)
    print(classify_report1)
    print(confusion_matrix1)

    #################plus f1 score########

if __name__ == "__main__":
    DoubleWindowMV(value,100,4,0.1,0.95)