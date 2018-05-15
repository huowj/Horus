# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
import numpy as np
import scipy.stats


"""
Algorithm3
"""
"""
initialize
"""
#miu_delta=0
#variation_delta=0
#M_delta=0
#sigma=0
#
with open("/hwj/yahoo/python/data/A1Benchmark/real_2.csv") as f:
  reader = csv.DictReader(f)
  value = [float(row['value']) for row in reader]
#value_length=len(value)
#
#def UpdateEstimation(k,delta_k_next):
#    delta=delta_k_next-miu_delta
#    miu_delta=miu_delta+delta/lamda_k_next
#    M_delta=lamda*M_delta+delta*(delta_k_next-miu_delta)
#    sigma=lamda*sigma+1
#    variation_delta=M_delta/sigma
    
"""
Algorithm2
"""
def SORAD(value,wide_of_window,epsilon,lamda):
    theta=[0]
    for i in range(1,wide_of_window+1):
        theta.append(pow(2,-i))
    theta=np.matrix(theta).T
    miu_delta=0
    M_delta=0
    sigma=0
#this variation has problemfirstly set it to 100
    variation_delta=9000
#juzhen initialize
    P=np.eye(wide_of_window+1)*500
    value_length=len(value)
    a_flag=[0]*value_length
    for k in range(wide_of_window,value_length-1):
        x_k=[1]
        for i in range(1,wide_of_window+1):
            x_k.append(value[k-i])
        x_k=np.matrix(x_k).T
        y_k_guji=theta.T*x_k
        delta_k=value[k]-y_k_guji
        z_epsilon=scipy.stats.norm(0,variation_delta).ppf(1-epsilon)
#        variation_delta=0
        if delta_k<(miu_delta-z_epsilon) or delta_k>(miu_delta+z_epsilon):
            a_flag[k]=1
            value[k]=y_k_guji
        else:
            P=(1/lamda)*P-(((1/lamda)*np.matrix(P)*x_k*(x_k.T)*np.matrix(P))/(1+(x_k.T)*np.matrix(P)*(x_k)))
            theta=(theta+delta_k.getA()[0][0]*(P*x_k))
#            variation_delta=0
#            miu_delta=0
#            M_delta=0
#            sigma=0
#            delta=delta_k-miu_delta
#            miu_delta=miu_delta+delta/(lamda*k+1)
#            M_delta=lamda*M_delta+delta*(delta_k-miu_delta)
#            sigma=lamda*sigma+1
#            variation_delta=M_delta/sigma
    print(a_flag)
    count=0
    for i in range(0,len(a_flag)-1):
        if a_flag[i]==1:
            print(i)
            count=count+1
    print("________________________________________")
    print(count)

if __name__ == "__main__":
    SORAD(value,3,0.000000001,0.9)
        
        
        
    
    
    