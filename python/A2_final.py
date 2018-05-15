#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 16:00:23 2018

@author: hwj
"""

"""
make them together
"""

#import csv
import math
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from sklearn import metrics

data=pd.read_csv("/hwj/yahoo/python/data/A2Benchmark/synthetic_40.csv")
value=data.value
is_anomaly=data.is_anomaly

def Norm(value,m,n,transition,p):
    #initialize mean and var
    T_length=len(value)
    T_dist=[0]*(T_length)
    T_dist_transition=[]
    for i in range(m,T_length-n+1):
        nearest_neighbor_dist=np.infty
        for j in range(i-m,i-n+1):
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
            pa=scipy.stats.norm(mean,var).ppf(p)
        if i>(m+transition):
            dist_now=nearest_neighbor_dist
            if dist_now>pa:
                print(i)
            else:
                q=i-m-transition-1
                var=var*(q+1)/(q+2)+(((dist_now-mean)**2)*(q+1))/((q+2)**2)
                mean=mean*(q+1)/(q+2)+dist_now/(q+1)
    print("the length of T_dist is:",len(T_dist))
    print("the length of T_dist_transition:",len(T_dist_transition))
    print("the final mean is:",mean)
    print("the final var is:",var)
    
    
    
def Lognorm(value,m,n,transition,p):
    T_length=len(value)
    T_dist=[0]*(T_length)
    T_dist_transition_log=[]
    for i in range(m,T_length-n+1):
        nearest_neighbor_dist=np.infty
        for j in range(i-m,i-n+1):
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
        if i>(m+transition):
            pa=scipy.stats.norm(mean_log,var_log).ppf(p)
            dist_now_log=T_dist_log
            if dist_now_log>pa:
                print(i)
            else:
                q=i-m-transition-1
                var_log=var_log*(q+1)/(q+2)+(((dist_now_log-mean_log)**2)*(q+1))/((q+2)**2)
                mean_log=mean_log*(q+1)/(q+2)+dist_now_log/(q+1)
    print("the length of T_dist is:",len(T_dist))
    print("the length of T_dist_transition_log is:",len(T_dist_transition_log))
    print("the final mean log is:",mean_log)
    print("the final var log is:",var_log)
        
if __name__ == "__main__":
    Norm(value,200,3,50,0.52)
    Lognorm(value,200,3,50,0.9995)

                
#def Distance(T_dist):
#    dist_length=len(T_dist)
#    zero_num=0
#    zero_num_tail=0
#    for i in range(dist_length):
#        if T_dist[i]==0:
#            zero_num+=1
#        else:
#            break
#    for i in range(dist_length):
#        if T_dist[dist_length-i-1]==0:
#            zero_num_tail+=1
#        else:
#            break
#    dist_no_zero=T_dist[zero_num:(dist_length-zero_num_tail)]
#    T_dist_log=[math.log(x) for x in dist_no_zero]
#    plt.figure(3)
#    plt.hist(T_dist[zero_num:dist_length],bins=200,density=1)
#    plt.savefig("/hwj/yahoo/distance/A2/plot/40_norm.jpg")
#    plt.figure(4)
#    plt.hist(T_dist_log,bins=200,density=1)
#    plt.savefig("/hwj/yahoo/distance/A2/plot/40_lognorm.jpg")
#    print("zero_num_pre:",zero_num)
#    print("zero_num_tail:",zero_num_tail)
    
    
#def norm(T_dist,transition,a):
#    dist_length=len(T_dist)
#    zero_num=0
#    zero_num_tail=0
#    for i in range(dist_length):
#        if T_dist[i]==0:
#            zero_num+=1
#        else:
#            break
#    for i in range(dist_length):
#        if T_dist[dist_length-i-1]==0:
#            zero_num_tail+=1
#        else:
#            break
#    T_dist_transition=T_dist[zero_num:zero_num+transition]
#    mean=np.mean(T_dist_transition)
#    var=np.var(T_dist_transition)
#    print("norm:")
#    print("norm mean:",mean)
#    print("norm var:",var)
#    for i in range(dist_length-zero_num-zero_num_tail-transition):
#        pa=scipy.stats.norm(mean,var).ppf(a)
#        dist_now=T_dist[i+zero_num+transition]
#        if dist_now>pa:
#            print(i+zero_num+transition)
#        else:
#            var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
#            mean=mean*(i+1)/(i+2)+dist_now/(i+1)
#    print("final norm mean:",mean)
#    print("final norm var:",var)
#            
#        
#        
#def lognorm(T_dist,transition,a):
#    dist_length=len(T_dist)
#    zero_num=0
#    zero_num_tail=0
#    for i in range(dist_length):
#        if T_dist[i]==0:
#            zero_num+=1
#        else:
#            break
#    for i in range(dist_length):
#        if T_dist[dist_length-i-1]==0:
#            zero_num_tail+=1
#        else:
#            break
#    dist_no_zero=T_dist[zero_num:(dist_length-zero_num_tail)]
#    T_dist_log=[math.log(x) for x in dist_no_zero]
#    T_dist_log_transition=T_dist_log[0:transition]
#    mean=np.mean(T_dist_log_transition)
#    var=np.mean(T_dist_log_transition)
#    print("lognorm:")
#    print("lognorm mean:",mean)
#    print("lognorm var:",var)
#    for i in range(dist_length-zero_num-zero_num_tail-transition):
#        pa=scipy.stats.norm(mean,var).ppf(a)
#        dist_now=T_dist_log[i+transition]
#        if dist_now>pa:
#            print(i+zero_num+transition)
#        else:
#            var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
#            mean=mean*(i+1)/(i+2)+dist_now/(i+1)
#    print("final lognorm mean:",mean)
#    print("final lognorm var:",var)
#    
#        
##def normForget(T_dist,transition,a,forget):
##def lognormForget(T_dist,transition,a,forget):  
##def F1(true,pred):
#    
#    
#if __name__ == "__main__":
#    a=DoubleWindow(value,200,3)
#    Distance(a)
#    norm(a,50,0.52)
#    lognorm(a,50,0.9999)