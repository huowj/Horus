#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:09:10 2018

@author: hwj
"""

"""
emmmm
begin from the simplest
so the simplest is A2 hhh
"""

#import csv
import math
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from sklearn import metrics

data=pd.read_csv("/hwj/yahoo/python/data/A2Benchmark/synthetic_4.csv")
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
    plt.savefig("/hwj/yahoo/distance/A2/plot/61_dist.jpg")
    plt.figure(2)
    plt.plot(x2,value)
    for i in x2:
        if is_anomaly[i]==1:
            plt.plot(i,value[i],'ro-')
    plt.savefig("/hwj/yahoo/distance/A2/plot/61_value.jpg")
    for i in x2:
        if is_anomaly[i]==1:
            print(i)
    T_dist_csv=pd.DataFrame(T_dist)
    T_dist_csv.to_csv("/hwj/yahoo/distance/A2/dist/61_dist.csv")
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
    plt.savefig("/hwj/yahoo/distance/A2/plot/61_norm.jpg")
    plt.figure(4)
    plt.hist(T_dist_log,bins=200,density=1)
    plt.savefig("/hwj/yahoo/distance/A2/plot/61_lognorm.jpg")
    print("zero_num_pre:",zero_num)
    print("zero_num_tail:",zero_num_tail)
    
    
def norm(T_dist,transition,a,lamda):
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
    T_dist_transition=T_dist[zero_num:zero_num+transition]
    mean=np.mean(T_dist_transition)
    var=np.var(T_dist_transition)
    print("norm:")
    print("norm mean:",mean)
    print("norm var:",var)
    index=1
    for i in range(dist_length-zero_num-zero_num_tail-transition):
        pa=scipy.stats.norm(mean,var).ppf(a)
        dist_now=T_dist[i+zero_num+transition]
        if dist_now>pa:
            print(i+zero_num+transition)
        else:
            index+=1
            var=var*lamda*(1-lamda**(index-1))/(1-lamda**index)+(np.square(dist_now-mean))*lamda*(1-lamda)*(1-lamda**(index-1))/np.square(1-lamda**(index))
            mean=dist_now*(1-lamda)/(1-lamda**(index))+mean*lamda*(1-lamda**(index-1))/(1-lamda**(index))
#            var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
#            mean=mean*(i+1)/(i+2)+dist_now/(i+1)
    print("final norm mean:",mean)
    print("final norm var:",var)
            
        
        
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
    dist_no_zero=T_dist[zero_num:(dist_length-zero_num_tail)]
    T_dist_log=[math.log(x) for x in dist_no_zero]
    T_dist_log_transition=T_dist_log[0:transition]
    mean=np.mean(T_dist_log_transition)
    var=np.var(T_dist_log_transition)
    print("lognorm:")
    print("lognorm mean:",mean)
    print("lognorm var:",var)
    for i in range(dist_length-zero_num-zero_num_tail-transition):
        pa=scipy.stats.norm(mean,var).ppf(a)
        dist_now=T_dist_log[i+transition]
        if dist_now>pa:
            print(i+zero_num+transition)
        else:
            var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
            mean=mean*(i+1)/(i+2)+dist_now/(i+1)
    print("final lognorm mean:",mean)
    print("final lognorm var:",var)
    
        
#def normForget(T_dist,transition,a,forget):
#def lognormForget(T_dist,transition,a,forget):  
#def F1(true,pred):
    
    
if __name__ == "__main__":
    a=DoubleWindow(value,100,3)
    Distance(a)
    norm(a,20,0.55,0.999999)
    #lognorm(a,20,0.999)