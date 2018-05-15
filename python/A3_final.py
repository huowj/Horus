#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 10:21:36 2018

@author: hwj
"""
"""
so it is the last one
I think it is really true
"""

#import csv
import math
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from sklearn import metrics

data=pd.read_csv("/hwj/yahoo/python/data/A3Benchmark/A3Benchmark-TS2.csv")
value=data.value
is_anomaly=data.anomaly

def Norm(value,m,n,transition,p):
    #initialize mean and var
    T_length=len(value)
    T_dist=[0]*(T_length)
    T_dist_transition=[]
    print("the initial anomaly:")
    anomaly_num=0
    for i in range(0,T_length):
        if is_anomaly[i]==1:
            print(i)
            anomaly_num+=1
    print("the anomaly num is:",anomaly_num)
    print("the anomaly after transition:" )
    anomaly_num_after_transition=0
    for i in range(T_length-m-transition):
        if is_anomaly[i+m+transition]==1:
            print(i+m+transition)
            anomaly_num_after_transition+=1
    print("the anomaly number after transition:",anomaly_num_after_transition)
    for i in range(m,T_length-n+1):
        nearest_neighbor_dist=np.infty
        for j in range(i-m,i-n+1):
            flag=0
            for f in range(n):
                if is_anomaly[j+f]==1:
                    flag=1
            if flag==0:
                a=np.array(value[i:i+n])
                b=np.array(value[j:j+n])
                dist=np.linalg.norm(a-b)
            if dist<nearest_neighbor_dist:
                nearest_neighbor_dist=dist
        T_dist[i]=nearest_neighbor_dist
        if i<(m+transition):
            T_dist_transition.append(nearest_neighbor_dist)
        if i==(m+transition):
            mean=np.mean(T_dist_transition)
            var=np.var(T_dist_transition)
            print("the initial mean is:",mean)
            print("the initial var is:",var)
        if i>=(m+transition):
            pa=scipy.stats.norm(mean,var).ppf(p)
            dist_now=nearest_neighbor_dist
            if dist_now>pa:
                print(i)
            else:
                q=i-m-transition
                var=var*(q+1)/(q+2)+(((dist_now-mean)**2)*(q+1))/((q+2)**2)
                mean=mean*(q+1)/(q+2)+dist_now/(q+1)
    print("the length of T_dist is:",len(T_dist))
    print("the length of T_dist_transition:",len(T_dist_transition))
    print("the final mean is:",mean)
    print("the final var is:",var)
#    x1=range(0,T_length)
#    plt.figure(1)
#    plt.plot(x1,T_dist)
    
    
    
def Lognorm(value,m,n,transition,p):
    T_length=len(value)
    T_dist=[0]*(T_length)
    T_dist_transition_log=[]
    print("the initial anomaly:")
    for i in range(0,T_length):
        if is_anomaly[i]==1:
            print(i)
    print("the anomaly after transition:" )
    for i in range(T_length-m-transition):
        if is_anomaly[i+m+transition]==1:
            print(i+m+transition)
    for i in range(m,T_length-n+1):
        nearest_neighbor_dist=np.infty
        for j in range(i-m,i-n+1):
            flag=0
            for f in range(n):
                if is_anomaly[j+f]==1:
                    flag=1
            if flag==0:
                a=np.array(value[i:i+n])
                b=np.array(value[j:j+n])
                dist=np.linalg.norm(a-b)
            if dist<nearest_neighbor_dist:
                nearest_neighbor_dist=dist
        T_dist[i]=nearest_neighbor_dist
        T_dist_log=math.log(nearest_neighbor_dist)
        if i<(m+transition):
            T_dist_transition_log.append(T_dist_log)
        if i==(m+transition):
            mean_log=np.mean(T_dist_transition_log)
            var_log=np.var(T_dist_transition_log)
            print("the initial meanlog is:",mean_log)
            print("the initial varlog is:",var_log)
        if i>=(m+transition):
            pa=scipy.stats.norm(mean_log,var_log).ppf(p)
            dist_now_log=T_dist_log
            if dist_now_log>pa:
                print(i)
            else:
                q=i-m-transition
                var_log=var_log*(q+1)/(q+2)+(((dist_now_log-mean_log)**2)*(q+1))/((q+2)**2)
                mean_log=mean_log*(q+1)/(q+2)+dist_now_log/(q+1)
    print("the length of T_dist is:",len(T_dist))
    print("the length of T_dist_transition_log is:",len(T_dist_transition_log))
    print("the final mean log is:",mean_log)
    print("the final var log is:",var_log)

        
if __name__ == "__main__":
    Norm(value,150,3,50,0.55)
    Lognorm(value,150,3,50,0.9999)