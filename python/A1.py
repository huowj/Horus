#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 12:38:36 2018

@author: hwj
"""


#import csv
import math
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from sklearn import metrics

data=pd.read_csv("/hwj/yahoo/python/data/A1Benchmark/real_26.csv")
value=data.value
is_anomaly=data.is_anomaly

def DoubleWindow(value,m,n):
    #initialize mean and var
    T_length=len(value)
    T_dist=[0]*(T_length)
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
    print("the length of T_dist is:",len(T_dist))
    x1=range(0,T_length)
    x2=range(0,T_length)
    plt.figure(1)
    plt.plot(x1,T_dist)
    plt.savefig("/hwj/yahoo/distance/A1/plot/26_dist.jpg")
    plt.figure(2)
    plt.plot(x2,value)
    for i in x2:
        if is_anomaly[i]==1:
            plt.plot(i,value[i],'ro-')
    plt.savefig("/hwj/yahoo/distance/A1/plot/26_value.jpg")
    anomaly_no=0
    for i in x2:
        if is_anomaly[i]==1:
            print(i)
            anomaly_no+=1
    print("anomaly number is:",anomaly_no)
    T_dist_csv=pd.DataFrame(T_dist)
    T_dist_csv.to_csv("/hwj/yahoo/distance/A1/dist/26_dist.csv")
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
    T_dist_log=[]
    for i in range(dist_length):
        if T_dist[i]>0:
            T_dist_log.append(math.log(T_dist[i]))
#    dist_no_zero=T_dist[zero_num:(dist_length-zero_num_tail)]
#    T_dist_log=[math.log(x) for x in dist_no_zero]
    plt.figure(3)
    plt.hist(T_dist[zero_num:dist_length],bins=200,density=1)
    plt.savefig("/hwj/yahoo/distance/A1/plot/26_norm.jpg")
    plt.figure(4)
    plt.hist(T_dist_log,bins=200,density=1)
    plt.savefig("/hwj/yahoo/distance/A1/plot/26_lognorm.jpg")
    print("zero_num_pre:",zero_num)
    print("zero_num_tail:",zero_num_tail)
    
    
def norm(T_dist,transition,a):
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
    anomaly_num_after_transition=0
    for i in range(dist_length-zero_num-transition):
        if is_anomaly[i+zero_num+transition]==1:
            print(i+zero_num+transition)
            anomaly_num_after_transition+=1
    T_dist_transition=T_dist[zero_num:zero_num+transition]
    #########################################################################
    #remove the anomaly in transition
#    for i in range(transition):
#        if is_anomaly[zero_num+i]==1:
#            del(T_dist_transition[i])
#            del(T_dist_transition[i-1])
#            del(T_dist_transition[i-2])
    #########################################################################
    mean=np.mean(T_dist_transition)
    var=np.var(T_dist_transition)
    print("norm:")
    print("norm mean:",mean)
    print("norm var:",var)
    for i in range(dist_length-zero_num-zero_num_tail-transition):
        pa=scipy.stats.norm(mean,var).ppf(a)
        dist_now=T_dist[i+zero_num+transition]
        if dist_now>36000:
            print(i+zero_num+transition)
        else:
            var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
            mean=mean*(i+1)/(i+2)+dist_now/(i+1)
    print("final norm mean:",mean)
    print("final norm var:",var)
    print("the num after transition:",anomaly_num_after_transition)
            
        
        
def lognorm(T_dist,transition,a):
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
    T_dist_log=[]
    for i in range(dist_length):
        if T_dist[i]>0:
            T_dist_log.append(math.log(T_dist[i]))
    num=0
    anomaly_num_after_transition=0
    T_dist_log_transition=[]
    for i in range(dist_length):
        if T_dist[i]>0:
            T_dist_log.append(math.log(T_dist[i]))
            num+=1
            if num<transition:
                T_dist_log_transition.append(math.log(T_dist[i]))
            if num==transition:
                mean=np.mean(T_dist_log_transition)
                var=np.var(T_dist_log_transition)
                print("initial lognorm mean:",mean)
                print("initial lognorm var:",var)
            if num>=transition:
                pa=scipy.stats.norm(mean,var).ppf(a)
                dist_now=math.log(T_dist[i])
                if dist_now>8.2:
                    print(i)
#               else:
#                   var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
#                   mean=mean*(i+1)/(i+2)+dist_now/(i+1)
    print("final lognorm mean:",mean)
    print("final lognorm var:",var)
    print("the anomaly after transition:",anomaly_num_after_transition)
    
        
#def normForget(T_dist,transition,a,forget):
#def lognormForget(T_dist,transition,a,forget):  
#def F1(true,pred):
    
    
if __name__ == "__main__":
    a=DoubleWindow(value,150,120)
    Distance(a)
    #norm(a,100,0.55)
    #lognorm(a,100,0.9999999)