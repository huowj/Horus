#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 10:53:46 2018

@author: hwj
"""


#import csv
import math
import numpy as np
import pandas as pd
import scipy.stats
#import matplotlib.pyplot as plt
from sklearn import metrics

#data=pd.read_csv("/hwj/yahoo/python/data/A3Benchmark/A3Benchmark-TS95.csv")
#value=data.value
#is_anomaly=data.anomaly

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
#    print("the length of T_dist is:",len(T_dist))
#    x1=range(0,T_length)
#    x2=range(0,T_length)
#    plt.figure(1)
#    plt.plot(x1,T_dist)
#    plt.savefig("/hwj/yahoo/distance/A2/plot/61_dist.jpg")
#    plt.figure(2)
#    plt.plot(x2,value)
#    for i in x2:
#        if is_anomaly[i]==1:
#            plt.plot(i,value[i],'ro-')
#    plt.savefig("/hwj/yahoo/distance/A2/plot/61_value.jpg")
#    for i in x2:
#        if is_anomaly[i]==1:
#            print(i)
#    T_dist_csv=pd.DataFrame(T_dist)
#    T_dist_csv.to_csv("/hwj/yahoo/distance/A2/dist/61_dist.csv")
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
#    dist_no_zero=T_dist[zero_num:(dist_length-zero_num_tail)]
#    T_dist_log=[math.log(x) for x in dist_no_zero]
#    plt.figure(3)
#    plt.hist(T_dist[zero_num:dist_length],bins=200,density=1)
#    plt.savefig("/hwj/yahoo/distance/A2/plot/61_norm.jpg")
#    plt.figure(4)
#    plt.hist(T_dist_log,bins=200,density=1)
#    plt.savefig("/hwj/yahoo/distance/A2/plot/61_lognorm.jpg")
#    print("zero_num_pre:",zero_num)
#    print("zero_num_tail:",zero_num_tail)
    
    
def norm(T_dist,transition,a):
    dist_length=len(T_dist)
#    norm_predict=[0]*(dist_length)
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
#    print("norm:")
#    print("norm mean:",mean)
#    print("norm var:",var)
    p_table=np.zeros((dist_length-zero_num-zero_num_tail-transition,7))
    for i in range(dist_length-zero_num-zero_num_tail-transition):
        pa=scipy.stats.norm(mean,var).ppf(a)
        dist_now=T_dist[i+zero_num+transition]
        p_table[i,0]=dist_now
        p_table[i,1]=mean
        p_table[i,2]=var
        p_table[i,3]=dist_length-zero_num-zero_num_tail-transition
        p_table[i,4]=scipy.stats.norm(mean,var).cdf(dist_now)
        p_table[i,5]=a
        p_table[i,6]=pa
#        if dist_now>pa:
#            norm_predict[i+zero_num+transition]=1
#        else:
#            var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
#            mean=mean*(i+1)/(i+2)+dist_now/(i+1)
    
    return(p_table)
#    print("final norm mean:",mean)
#    print("final norm var:",var)
            
        
        
def lognorm(T_dist,transition,a):
    dist_length=len(T_dist)
    lognorm_predict=[0]*dist_length
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
#    print("lognorm:")
#    print("lognorm mean:",mean)
#    print("lognorm var:",var)
    for i in range(dist_length-zero_num-zero_num_tail-transition):
        pa=scipy.stats.norm(mean,var).ppf(a)
        dist_now=T_dist_log[i+transition]
        if dist_now>pa:
            lognorm_predict[i+zero_num+transition]=1
        else:
            var=var*(i+1)/(i+2)+(((dist_now-mean)**2)*(i+1))/((i+2)**2)
            mean=mean*(i+1)/(i+2)+dist_now/(i+1)
    return(lognorm_predict)
#    print("final lognorm mean:",mean)
#    print("final lognorm var:",var)
    
        
#def normForget(T_dist,transition,a,forget):
#def lognormForget(T_dist,transition,a,forget):  
#def F1(true,pred):
    
    
if __name__ == "__main__":
    A2_p=pd.read_csv("/hwj/yahoo/distance/tricks/A3.csv")
    norm_window=A2_p.norm_window
    norm_a=A2_p.norm_a
    norm_transition=A2_p.norm_transition
    norm_sub=A2_p.norm_sub
    table=np.zeros((100,3))
    for i in range(100):
        data=pd.read_csv("/hwj/yahoo/python/data/A3Benchmark/A3Benchmark-TS"+str(i+1)+".csv")
        value=data.value
        is_anomaly=data.anomaly
        a=DoubleWindow(value,norm_window[i],norm_sub[i])
        predict=norm(a,norm_transition[i],norm_a[i])
#        for m in range(4,len(predict)-3):
#            if (is_anomaly[m]==1):
#                flag=0
#                for j in range(-3,3):
#                    if(predict[j+m]==1):
#                        flag=1
#                if (flag==1):
#                    for q in range(-3,3):
#                        predict[m+q]=is_anomaly[m+q]
#        for q in range(norm_window[i]+norm_transition[i]):
#            is_anomaly[q]=0
#        conf_mat = metrics.confusion_matrix(is_anomaly, predict)
#        tp=conf_mat[1,1]
#        fn=conf_mat[0,1]
#        fp=conf_mat[1,0]
#        table[i,0]=tp
#        table[i,1]=fn
#        table[i,2]=fp
        print(i)
        np.savetxt("/hwj/yahoo/distance/A3/probability/A3_probability_"+str(i+1)+".csv", predict, delimiter = ',')