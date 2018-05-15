#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 20:28:53 2017

@author: hwj
"""

import csv
import numpy as np

with open("/hwj/yahoo/python/data/A1Benchmark/real_3.csv") as f:
  reader = csv.DictReader(f)
  value = [float(row['value']) for row in reader]
  
def Brute_Force(value,n):
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
                if dist<nearest_neighbor_dist:
                    nearest_neighbor_dist=dist
        if nearest_neighbor_dist>best_so_far_dist:
            best_so_far_dist=nearest_neighbor_dist
            best_so_far_loc=i
    return(best_so_far_dist,best_so_far_loc)

if __name__ == "__main__":
    print(Brute_Force(value,3))
    
                
               
                
                
                