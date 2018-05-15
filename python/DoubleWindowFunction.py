#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 10:31:17 2018

@author: hwj
"""

#import csv
import math
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from sklearn import metrics

data=pd.read_csv("/hwj/yahoo/python/data/A1Benchmark/real_29.csv")
value=data.value
is_anomaly=data.is_anomaly

#with open("/hwj/yahoo/python/data/A1Benchmark/real_5.csv") as f:
#  reader = csv.DictReader(f)
#  value = [float(row['value']) for row in reader]

def DoubleWindow(value,m,n):
    #initialize mean and var
    T_length=len(value)
    T_dist=[0]*(T_length)
    for i in range(m,T_length-n+1):
        nearest_neighbor_dist=np.infty
        for j in range(i-m,i-n+1):
            a=np.array(value[i:i+n])
            b=np.array(value[j:j+n])
            dist=np.linalg.norm(a-b)
            if dist<nearest_neighbor_dist:
                nearest_neighbor_dist=dist
        T_dist[i]=nearest_neighbor_dist
    print(len(T_dist))
    x1=range(0,T_length)
    x2=range(0,T_length)
    plt.figure(1)
    plt.plot(x1,T_dist)
    plt.figure(2)
    plt.plot(x2,value)
    for i in x2:
        if is_anomaly[i]==1:
            plt.plot(i,value[i],'ro-')
    T_dist_csv=pd.DataFrame(T_dist)
    T_dist_csv.to_csv("/hwj/yahoo/python/dist/A2/synthetic_2_dist.csv")
    return(T_dist)

def Distance(T_dist):
    dist_length=len(T_dist)
    zero_num=0
    zero_num_tail=0
    for i in range(dist_length):
        if T_dist[i]==0:
            zero_num+=1
        else:
            break
    for i in range(dist_length):
        if T_dist[dist_length-i-1]==0:
            zero_num_tail+=1
        else:
            break
    dist_no_zero=T_dist[zero_num:(dist_length-zero_num_tail)]
    T_dist_log=[math.log(x) for x in dist_no_zero]
    plt.figure(3)
    plt.hist(T_dist[zero_num:dist_length],bins=200,density=1)
    plt.figure(4)
    plt.hist(T_dist_log,bins=200,density=1)
    print(zero_num)
    print(zero_num_tail)
    return(zero_num)
    
#def 
    
if __name__ == "__main__":
    a=DoubleWindow(value,100,4)
    Distance(a)