#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 12:45:53 2017

@author: hwj
"""

#import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv("/hwj/yahoo/python/data/A1Benchmark/real_3.csv")
value=data.value
is_anomaly=data.is_anomaly

def Heuristic_Search(value,n):
    best_so_far_dist=0
    best_so_far_loc=np.NaN
    T_length=len(value)
    
    for i in range(0,T_length-n+1):
        nearest_neighbor_dist=np.infty
        for j in range(0,T_length-n+1):
            if abs(i-j)>=n:
                a=np.array(value[i:i+n])
                b=np.array(value[j:j+n])
                dist=np.linalg.norm(a - b)
                if dist<best_so_far_dist:
                    nearest_neighbor_dist=dist #heihei
                    break
                if dist<nearest_neighbor_dist:
                    nearest_neighbor_dist=dist
        if nearest_neighbor_dist>best_so_far_dist:
            best_so_far_dist=nearest_neighbor_dist
            best_so_far_loc=i
    print(best_so_far_dist,best_so_far_loc)
    return(best_so_far_dist,best_so_far_loc)

if __name__ == "__main__":
    Heuristic_Search(value,3)
    