#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 13:41:11 2017

@author: hwj
"""

#import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv("/hwj/yahoo/python/data/A1Benchmark/real_29.csv")
value=data.value
is_anomaly=data.is_anomaly

#with open("/hwj/yahoo/python/data/A1Benchmark/real_5.csv") as f:
#  reader = csv.DictReader(f)
#  value = [float(row['value']) for row in reader]

def DoubleWindow(value,m,n):
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
    x1=range(len(T_dist))
    x2=range(len(value))
    plt.figure(1)
    plt.plot(x1,T_dist)
    plt.figure(2)
    plt.plot(x2,value)
    for i in x2:
        if is_anomaly[i]==1:
            plt.plot(i,value[i],'ro-')
 
#def Brute_Force(value,is_anomaly,n):
##    best_so_far_dist=0
##    best_so_far_loc=np.NaN
#    T_length=len(value)
#    T_dist=[-1]*(T_length-n+1)
#    for i in range(0,T_length-n+1):
#        nearest_neighbor_dist=np.infty
#        for j in range(0,T_length-n+1):
#            if abs(i-j)>=n:
#                a=np.array(value[i:i+n])
#                b=np.array(value[j:j+n])
#                dist=np.linalg.norm(a - b)
#                if dist<nearest_neighbor_dist:
#                    nearest_neighbor_dist=dist
#        T_dist[i]=nearest_neighbor_dist
##        if nearest_neighbor_dist>best_so_far_dist:
##            best_so_far_dist=nearest_neighbor_dist
##            best_so_far_loc=i
##    print(T_dist)
#    print(len(T_dist))
#    x1=range(len(T_dist))
#    x2=range(len(value))
#    plt.figure(1)
#    plt.plot(x1,T_dist)
#    plt.savefig("/hwj/yahoo/python/BruteForce/plot/46_real_dist.jpg")
#    plt.figure(2)
#    plt.plot(x2,value)
#    for i in x2:
#        if is_anomaly[i]==1:
#            plt.plot(i,value[i],'ro-')
#    plt.savefig("/hwj/yahoo/python/BruteForce/plot/46_real.jpg")
#    for i in range(0,len(T_dist)):
#        if T_dist[i]>0.2:
#            print(T_dist[i],i)
#    for i in range(0,len(value)):
#        if is_anomaly[i]==1:
#            print(i)

if __name__ == "__main__":
    DoubleWindow(value,100,3)