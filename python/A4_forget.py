#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 18:34:50 2018

@author: hwj
"""

#import csv
import math
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from sklearn import metrics

data=pd.read_csv("/hwj/yahoo/python/data/A4Benchmark/A4Benchmark-TS91.csv")
value=data.value
is_anomaly=data.anomaly

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
    plt.savefig("/hwj/yahoo/distance/A4/plot/91_dist.jpg")
    plt.figure(2)
    plt.plot(x2,value)
    for i in x2:
        if is_anomaly[i]==1:
            plt.plot(i,value[i],'ro-')
    plt.savefig("/hwj/yahoo/distance/A4/plot/91_value.jpg")
    anomaly_no=0
    for i in x2:
        if is_anomaly[i]==1:
            print(i)
            anomaly_no+=1
    print("anomaly number is:",anomaly_no)
    T_dist_csv=pd.DataFrame(T_dist)
    T_dist_csv.to_csv("/hwj/yahoo/distance/A4/dist/91_dist.csv")
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
    plt.savefig("/hwj/yahoo/distance/A4/plot/91_norm.jpg")
    plt.figure(4)
    plt.hist(T_dist_log,bins=200,density=1)
    plt.savefig("/hwj/yahoo/distance/A4/plot/91_lognorm.jpg")
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
    index=2
    print("norm:")
    print("norm mean:",mean)
    print("norm var:",var)
    for i in range(dist_length-zero_num-zero_num_tail-transition):
        pa=scipy.stats.norm(mean,var).ppf(a)
        dist_now=T_dist[i+zero_num+transition]
        if dist_now>pa:
            print(i+zero_num+transition)
        else:
            var=var*lamda*(1-lamda**(index-1))/(1-lamda**index)+(np.square(dist_now-mean))*lamda*(1-lamda)*(1-lamda**(index-1))/np.square(1-lamda**(index))
            mean=dist_now*(1-lamda)/(1-lamda**(index))+mean*lamda*(1-lamda**(index-1))/(1-lamda**(index))
#        else:
#            var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
#            mean=mean*(i+1)/(i+2)+dist_now/(i+1)
    print("final norm mean:",mean)
    print("final norm var:",var)
    print("the num after transition:",anomaly_num_after_transition)
            
        
        
def lognorm(T_dist,transition,a,lamda):
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
    dist_no_zero=T_dist[zero_num:(dist_length-zero_num_tail)]
    T_dist_log=[math.log(x) for x in dist_no_zero]
    T_dist_log_transition=T_dist_log[0:transition]
    #########################################################################
    #remove the anomaly in transition
#    for i in range(transition):
#        if is_anomaly[zero_num+i]==1:
#            del(T_dist_log_transition[i])
#            del(T_dist_log_transition[i-1])
#            del(T_dist_log_transition[i-2])
    #########################################################################
    mean=np.mean(T_dist_log_transition)
    var=np.var(T_dist_log_transition)
    print("lognorm:")
    print("lognorm mean:",mean)
    print("lognorm var:",var)
    mean_array=[]
    var_array=[]
    pa_array=[]
    mean_array.append(mean)
    var_array.append(var)
    pa_array.append(0)
    index=1
    for i in range(dist_length-zero_num-zero_num_tail-transition):
        pa=scipy.stats.norm(mean,var).ppf(a)
        pa_array.append(pa)
        dist_now=T_dist_log[i+transition]
        if dist_now>pa:
            print(i+zero_num+transition)
        else:
            index+=1
            var=var*lamda*(1-lamda**(index-1))/(1-lamda**index)+(np.square(dist_now-mean))*lamda*(1-lamda)*(1-lamda**(index-1))/np.square(1-lamda**(index))
            mean=dist_now*(1-lamda)/(1-lamda**(index))+mean*lamda*(1-lamda**(index-1))/(1-lamda**(index))
#        else:
#            var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
#            mean=mean*(i+1)/(i+2)+dist_now/(i+1)
#            mean_array.append(mean)
#            var_array.append(var)
#            pa_array.append(pa)
#    mean_var_csv=pd.DataFrame(mean_array,var_array,pa_array)
#    mean_var_csv.to_csv("/hwj/yahoo/distance/A3/dist/28_mean_var.csv")
    print("final lognorm mean:",mean)
    print("final lognorm var:",var)
    print("the anomaly after transition:",anomaly_num_after_transition)
    
        
#def normForget(T_dist,transition,a,forget):
#def lognormForget(T_dist,transition,a,forget):  
#def F1(true,pred):
    
    
if __name__ == "__main__":
    a=DoubleWindow(value,200,3)
    Distance(a)
    norm(a,100,0.999,0.99)
    #lognorm(a,50,0.99999999999)